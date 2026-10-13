# app/email_service.py
# ─────────────────────────────────────────────────────────────────────────────
# Servicio de envío de correos electrónicos (SMTP).
#
# Configuración por variables de entorno (nunca hardcodear credenciales):
#   MAIL_HOST     — servidor SMTP          (default: smtp.gmail.com)
#   MAIL_PORT     — puerto SMTP            (default: 587)
#   MAIL_USER     — cuenta remitente       (requerido en producción)
#   MAIL_PASSWORD — contraseña / app-key   (requerido en producción)
#   MAIL_FROM     — dirección From         (default: igual a MAIL_USER)
#
# En desarrollo, si MAIL_USER no está configurado, los envíos se simulan
# imprimiendo en consola (modo DRY-RUN) para no bloquear el flujo.
# ─────────────────────────────────────────────────────────────────────────────

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


# ── Función base de envío ─────────────────────────────────────────────────────

def send_email(to: str, subject: str, html_body: str) -> bool:
    """
    Envía un correo HTML.
    Retorna True si el envío fue exitoso, False en caso de error.
    En modo DRY-RUN imprime en consola y retorna True (no bloquea el flujo).
    Las variables se leen en tiempo de ejecución para respetar load_dotenv().
    """
    mail_host     = os.getenv("MAIL_HOST",     "smtp.gmail.com")
    mail_port     = int(os.getenv("MAIL_PORT", "587"))
    mail_user     = os.getenv("MAIL_USER",     "")
    mail_password = os.getenv("MAIL_PASSWORD", "")
    mail_from     = os.getenv("MAIL_FROM",     mail_user)

    if not mail_user:
        logger.info(
            "[EMAIL DRY-RUN] To: %s | Subject: %s\n%s",
            to, subject, html_body
        )
        return True

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = mail_from
    msg["To"]      = to
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(mail_host, mail_port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.login(mail_user, mail_password)
            server.sendmail(mail_from, [to], msg.as_string())
        logger.info("Email enviado a %s — %s", to, subject)
        return True
    except smtplib.SMTPAuthenticationError:
        logger.error("Error SMTP: credenciales incorrectas para %s", mail_user)
    except smtplib.SMTPException as exc:
        logger.error("Error SMTP al enviar a %s: %s", to, exc)
    except OSError as exc:
        logger.error("Error de red al conectar a %s:%s — %s", mail_host, mail_port, exc)
    return False


# ── Plantillas de correo ──────────────────────────────────────────────────────

def _base_url() -> str:
    """Retorna la URL base del frontend para enlaces de notificación por correo."""
    return os.getenv("BASE_URL", "http://localhost:5173").rstrip("/")


def send_bienvenida(to: str, nombre: str) -> bool:
    """Correo de bienvenida tras registro exitoso."""
    base = _base_url()
    subject = "¡Bienvenido a driven yield Pro! 🚗"
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;padding:24px;
                background:#0a0a0a;color:#e0e0e0;border-radius:12px;
                border:1px solid rgba(220,38,38,0.2)">
      <h2 style="color:#dc2626;margin-bottom:4px">driven yield <span style="color:#fff">Pro</span></h2>
      <p style="color:rgba(255,255,255,0.4);font-size:12px;margin-top:0">Sistema de gestión automotriz</p>
      <hr style="border-color:rgba(220,38,38,0.15);margin:16px 0">
      <p>Hola <strong style="color:#fff">{nombre}</strong>,</p>
      <p>Tu cuenta ha sido creada exitosamente. Ya puedes agendar citas, revisar
         el historial de tu vehículo y mucho más.</p>
      <a href="{base}"
         style="display:inline-block;margin-top:16px;padding:12px 24px;
                background:#dc2626;color:#fff;text-decoration:none;
                border-radius:8px;font-weight:bold">
        Ir al sistema
      </a>
      <p style="margin-top:24px;font-size:11px;color:rgba(255,255,255,0.25)">
        Si no creaste esta cuenta, ignora este correo.
      </p>
    </div>
    """
    return send_email(to, subject, html)


def send_cita_confirmada(to: str, nombre: str, servicio: str, fecha: str, hora: str) -> bool:
    """Correo cuando se agenda una nueva cita."""
    subject = "Cita agendada en driven yield ✅"
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;padding:24px;
                background:#0a0a0a;color:#e0e0e0;border-radius:12px;
                border:1px solid rgba(220,38,38,0.2)">
      <h2 style="color:#dc2626">driven yield <span style="color:#fff">Pro</span></h2>
      <hr style="border-color:rgba(220,38,38,0.15);margin:16px 0">
      <p>Hola <strong style="color:#fff">{nombre}</strong>,</p>
      <p>Tu cita ha sido registrada con los siguientes datos:</p>
      <table style="width:100%;border-collapse:collapse;margin:12px 0">
        <tr style="border-bottom:1px solid rgba(255,255,255,0.08)">
          <td style="padding:8px;color:rgba(255,255,255,0.4);font-size:13px">Servicio</td>
          <td style="padding:8px;color:#fff;font-weight:bold">{servicio}</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.08)">
          <td style="padding:8px;color:rgba(255,255,255,0.4);font-size:13px">Fecha</td>
          <td style="padding:8px;color:#fff">{fecha}</td>
        </tr>
        <tr>
          <td style="padding:8px;color:rgba(255,255,255,0.4);font-size:13px">Hora</td>
          <td style="padding:8px;color:#fff">{hora}</td>
        </tr>
      </table>
      <p style="color:rgba(255,255,255,0.4);font-size:12px">
        Nuestro equipo confirmará tu cita a la brevedad. Si necesitas cancelar,
        puedes hacerlo desde tu perfil.
      </p>
    </div>
    """
    return send_email(to, subject, html)


def send_recuperacion_contrasena(to: str, nombre: str, token_reset: str) -> bool:
    """
    Correo de recuperación de contraseña.
    El enlace lleva el token como query param; el frontend debe tener
    una ruta /reset-password?token=XXX que llame a POST /api/auth/reset-password.
    """
    subject = "Recuperación de contraseña — driven yield"
    base    = _base_url()
    link    = f"{base}/reset-password?token={token_reset}"
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;padding:24px;
                background:#0a0a0a;color:#e0e0e0;border-radius:12px;
                border:1px solid rgba(220,38,38,0.2)">
      <h2 style="color:#dc2626">driven yield <span style="color:#fff">Pro</span></h2>
      <hr style="border-color:rgba(220,38,38,0.15);margin:16px 0">
      <p>Hola <strong style="color:#fff">{nombre}</strong>,</p>
      <p>Recibimos una solicitud para restablecer tu contraseña.
         Haz clic en el botón de abajo. El enlace expira en <strong>1 hora</strong>.</p>
      <a href="{link}"
         style="display:inline-block;margin-top:16px;padding:12px 24px;
                background:#dc2626;color:#fff;text-decoration:none;
                border-radius:8px;font-weight:bold">
        Restablecer contraseña
      </a>
      <p style="margin-top:24px;font-size:11px;color:rgba(255,255,255,0.25)">
        Si no solicitaste este cambio, ignora este correo. Tu contraseña no será modificada.
      </p>
    </div>
    """
    return send_email(to, subject, html)