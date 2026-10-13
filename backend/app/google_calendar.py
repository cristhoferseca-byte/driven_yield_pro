import os
import datetime
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'service_account.json')

def get_calendar_service() -> any:
    """
    Autentica y retorna el servicio de Google Calendar usando una Service Account.
    Retorna None si el archivo service_account.json no existe.
    """
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        logger.warning(f"No se encontró el archivo de credenciales de Google Calendar en: {SERVICE_ACCOUNT_FILE}")
        return None

    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        logger.error(f"Error al inicializar el servicio de Google Calendar: {str(e)}")
        return None

def crear_evento_cita(cita_data):
    """
    Crea un evento en Google Calendar para una cita agendada.
    Se ejecuta en el calendario principal (primary) de la cuenta de servicio.
    
    cita_data debe contener:
    - id: int
    - cliente: str
    - email: str
    - vehiculo: str
    - placa: str
    - servicio: str
    - fecha: str (YYYY-MM-DD)
    - hora: str (HH:MM)
    - notas: str
    """
    service = get_calendar_service()
    if not service:
        return False
        
    try:
        # Combinar fecha y hora para el inicio
        start_datetime_str = f"{cita_data['fecha']}T{cita_data['hora']}:00"
        start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%S")
        
        # Asumimos que cada cita dura 1 hora por defecto (se puede mejorar dependiendo del servicio)
        end_datetime = start_datetime + datetime.timedelta(hours=1)

        event = {
            'summary': f"Cita Taller: {cita_data['cliente']} - {cita_data['servicio']}",
            'location': 'Taller Automotriz Driven Yield',
            'description': (
                f"Servicio: {cita_data['servicio']}\n"
                f"Cliente: {cita_data['cliente']}\n"
                f"Email: {cita_data.get('email', 'N/A')}\n"
                f"Vehículo: {cita_data['vehiculo']} (Placa: {cita_data['placa']})\n"
                f"Notas adicionales: {cita_data.get('notas', 'Ninguna')}"
            ),
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'America/Bogota', # Cambiar si es otra zona horaria
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'America/Bogota',
            },
            # Si quieres que le llegue invitación al cliente:
            'attendees': [
                {'email': cita_data.get('email')}
            ] if cita_data.get('email') else [],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 60},
                ],
            },
        }

        # Insertar evento en el calendario principal de la Service Account
        # Ojo: si quieres insertarlo en tu calendario personal usando una service account,
        # debes compartir tu calendario personal con el correo de la service account y usar tu ID de calendario aquí.
        calendar_id = 'primary'
        
        event_result = service.events().insert(calendarId=calendar_id, body=event).execute()
        logger.info(f"Evento de Google Calendar creado: {event_result.get('htmlLink')}")
        return True

    except Exception as e:
        logger.error(f"Ocurrió un error al crear el evento en Google Calendar: {str(e)}")
        return False

def buscar_evento_cita(service, cita_data):
    """Busca un evento en Google Calendar basado en fecha, hora y cliente."""
    try:
        start_datetime_str = f"{cita_data['fecha']}T{cita_data['hora']}:00"
        start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%S")
        # Extend search window slightly to ensure we catch it
        time_min = (start_datetime - datetime.timedelta(minutes=10)).isoformat() + '-05:00'
        time_max = (start_datetime + datetime.timedelta(hours=1, minutes=10)).isoformat() + '-05:00'
        
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=time_min, 
            timeMax=time_max, 
            q=cita_data['cliente'],
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        if events:
            return events[0]['id'] # Retorna el ID del primer evento que coincide
        return None
    except Exception as e:
        logger.error(f"Error al buscar evento: {str(e)}")
        return None

def eliminar_evento_cita(cita_data: dict) -> bool:
    """Elimina el evento correspondiente a la cita en Google Calendar si existe."""
    service = get_calendar_service()
    if not service:
        return False
    
    event_id = buscar_evento_cita(service, cita_data)
    if event_id:
        try:
            service.events().delete(calendarId='primary', eventId=event_id).execute()
            logger.info(f"Evento eliminado de Google Calendar: {event_id}")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar evento: {str(e)}")
            return False
    return False

def actualizar_evento_cita(cita_antigua: dict, cita_nueva: dict) -> bool:
    """Actualiza la fecha, hora o descripción de un evento existente en Google Calendar."""
    service = get_calendar_service()
    if not service:
        return False
    
    event_id = buscar_evento_cita(service, cita_antigua)
    if event_id:
        try:
            start_datetime_str = f"{cita_nueva['fecha']}T{cita_nueva['hora']}:00"
            start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%S")
            end_datetime = start_datetime + datetime.timedelta(hours=1)

            event = service.events().get(calendarId='primary', eventId=event_id).execute()
            
            event['summary'] = f"Cita Taller: {cita_nueva['cliente']} - {cita_nueva.get('servicio', '')}"
            event['start']['dateTime'] = start_datetime.isoformat()
            event['end']['dateTime'] = end_datetime.isoformat()
            
            updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
            logger.info(f"Evento actualizado: {updated_event.get('htmlLink')}")
            return True
        except Exception as e:
            logger.error(f"Error al actualizar evento: {str(e)}")
            return False
    else:
        # Si no existía, lo creamos
        return crear_evento_cita(cita_nueva)

