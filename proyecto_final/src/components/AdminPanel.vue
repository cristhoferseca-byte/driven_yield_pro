<template>
  <div class="admin-wrapper">
    <!-- TABS -->
    <div class="panel-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="panel-tab"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>

    <!-- ===== SECCIÓN CITAS ===== -->
    <div v-if="activeTab === 'citas'" class="panel-section">
      <!-- Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-number white">{{ citas.length }}</div>
            <div class="stat-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
          </div>
          <div class="stat-label">TOTAL CITAS</div>
          <div class="stat-bar" style="background:rgba(255,255,255,.15)"></div>
        </div>
        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-number yellow">{{ citasPor('pendiente') }}</div>
            <div class="stat-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
          </div>
          <div class="stat-label">PENDIENTES</div>
          <div class="stat-bar" style="background:rgba(245,158,11,.3)"></div>
        </div>
        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-number blue">{{ citasPor('confirmada') }}</div>
            <div class="stat-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
          </div>
          <div class="stat-label">CONFIRMADAS</div>
          <div class="stat-bar" style="background:rgba(59,130,246,.3)"></div>
        </div>
        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-number green">{{ citasPor('completada') }}</div>
            <div class="stat-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
          </div>
          <div class="stat-label">COMPLETADAS</div>
          <div class="stat-bar" style="background:rgba(16,185,129,.3)"></div>
        </div>
        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-number red">{{ citasPor('cancelada') }}</div>
            <div class="stat-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
          </div>
          <div class="stat-label">CANCELADAS</div>
          <div class="stat-bar" style="background:rgba(220,38,38,.3)"></div>
        </div>
      </div>

      <!-- Toolbar -->
      <div class="table-toolbar">
        <div class="filter-tags">
          <button
            v-for="f in filtrosCitas"
            :key="f.value"
            class="filter-tag"
            :class="{ active: filtroCitas === f.value }"
            @click="filtroCitas = f.value"
          >
            {{ f.label }}
          </button>
        </div>
        <div class="toolbar-actions">
          <input
            v-model="searchCitas"
            type="text"
            class="search-input"
            placeholder="Buscar cliente o servicio..."
          />
          <button class="btn-red" @click="abrirModalCita()">+ NUEVA CITA</button>
          <button class="btn-ghost" @click="exportarCSV"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg> EXPORTAR</button>
        </div>
      </div>

      <!-- Tabla -->
      <div class="table-container">
        <div v-if="!citasFiltradas.length" class="empty-state">
          <span class="empty-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>️</span>
          <h3>Sin citas</h3>
          <p>Aún no hay citas registradas en el sistema</p>
          <button class="btn-red" @click="abrirModalCita()">+ Crear primera cita</button>
        </div>
        <table v-else class="table">
          <thead>
            <tr>
              <th>#</th><th>CLIENTE</th><th>SERVICIO</th>
              <th>FECHA</th><th>HORA</th><th>ESTADO</th><th>ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(cita, i) in citasFiltradas" :key="cita.id">
              <td>{{ String(i + 1).padStart(2, '0') }}</td>
              <td>
                <div class="cliente-cell">
                  <div class="avatar">{{ cita.cliente[0].toUpperCase() }}</div>
                  <div>
                    <div class="cliente-nombre">{{ cita.cliente }}</div>
                    <div v-if="cita.email" class="cliente-email">{{ cita.email }}</div>
                  </div>
                </div>
              </td>
              <td>{{ cita.servicio }}</td>
              <td>{{ formatFecha(cita.fecha) }}</td>
              <td>{{ cita.hora }}</td>
              <td><span :class="['badge', `badge-${cita.estado}`]">{{ cita.estado }}</span></td>
              <td>
                <div class="acciones-cell">
                  <select
                    class="status-select"
                    :value="cita.estado"
                    @change="cambiarEstado(cita.id, $event.target.value)"
                  >
                    <option value="pendiente">Pendiente</option>
                    <option value="confirmada">Confirmada</option>
                    <option value="completada">Completada</option>
                    <option value="cancelada">Cancelada</option>
                  </select>
                  <button class="action-btn" @click="abrirModalCita(cita)"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>️</button>
                  <button class="action-btn" @click="eliminarCita(cita.id)"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ===== SECCIÓN VENTAS ===== -->
    <div v-if="activeTab === 'ventas'" class="panel-section">
      <!-- Stats ventas -->
      <div class="ventas-stats">
        <div class="venta-stat-card rojo">
          <div class="vs-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
          <div class="vs-label">INGRESOS MES</div>
          <div class="vs-value">{{ fmtCOP(ingresosMes) }}</div>
          <div :class="['vs-change', cambioPct >= 0 ? 'pos' : 'neg']">
            {{ cambioPct >= 0 ? '▲' : '▼' }} {{ Math.abs(cambioPct) }}% vs mes anterior
          </div>
        </div>
        <div class="venta-stat-card verde">
          <div class="vs-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
          <div class="vs-label">SERVICIOS MES</div>
          <div class="vs-value">{{ ventasMes.length }}</div>
          <div class="vs-sub">servicios completados</div>
        </div>
        <div class="venta-stat-card azul">
          <div class="vs-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
          <div class="vs-label">TICKET PROMEDIO</div>
          <div class="vs-value">{{ fmtCOP(ticketPromedio) }}</div>
          <div class="vs-sub">por servicio</div>
        </div>
        <div class="venta-stat-card amarillo">
          <div class="vs-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></div>
          <div class="vs-label">TOP SERVICIO</div>
          <div class="vs-value" style="font-size:1.3rem">{{ topServicio }}</div>
          <div class="vs-sub">más solicitado</div>
        </div>
      </div>

      <!-- Grid ventas row 1 -->
      <div class="ventas-grid">
        <!-- Barras mensuales -->
        <div class="v-card">
          <div class="v-card-header">
            <span class="v-card-title">INGRESOS MENSUALES</span>
            <span class="v-card-badge">Últimos 6 meses</span>
          </div>
          <div class="bar-chart-wrap">
            <div v-for="(mes, i) in datosMensuales" :key="i" class="bar-col">
              <div
                class="bar-fill"
                :class="{ highlight: i === datosMensuales.length - 1 }"
                :style="{ height: barHeight(mes.total) + 'px' }"
              >
                <span class="bar-tooltip">{{ fmtCOP(mes.total) }}</span>
              </div>
              <span class="bar-label">{{ mes.label }}</span>
            </div>
          </div>
        </div>

        <!-- Venta rápida -->
        <div class="v-card">
          <div class="v-card-header">
            <span class="v-card-title">REGISTRAR VENTA</span>
          </div>
          <div class="quick-sale-form">
            <div class="qs-group">
              <label>Cliente *</label>
              <input v-model="qsCliente" type="text" placeholder="Nombre del cliente" class="qs-input" />
            </div>
            <div class="qs-row">
              <div class="qs-group">
                <label>Servicio *</label>
                <select v-model="qsServicio" class="qs-input" @change="autoFillPrecio">
                  <option value="">Seleccionar...</option>
                  <option v-for="s in servicios" :key="s.id" :value="s.nombre">{{ s.nombre }}</option>
                </select>
              </div>
              <div class="qs-group">
                <label>Método de pago</label>
                <select v-model="qsMetodo" class="qs-input">
                  <option>Efectivo</option>
                  <option>Transferencia</option>
                  <option>Tarjeta</option>
                </select>
              </div>
            </div>
            <div class="qs-group">
              <label>Monto ($) *</label>
              <input v-model.number="qsMonto" type="number" placeholder="0" class="qs-input" />
            </div>
            <div class="qs-total">
              <span class="qs-total-label">Total a cobrar</span>
              <span class="qs-total-value">{{ fmtCOP(qsMonto || 0) }}</span>
            </div>
            <button class="btn-red btn-full" @click="registrarVenta"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg> REGISTRAR VENTA</button>
          </div>
        </div>
      </div>

      <!-- Grid ventas row 2 -->
      <div class="ventas-grid">
        <!-- Top servicios -->
        <div class="v-card">
          <div class="v-card-header">
            <span class="v-card-title">TOP SERVICIOS POR INGRESOS</span>
          </div>
          <div class="service-bars">
            <div v-for="(item, i) in topServicios" :key="i" class="service-bar-item">
              <div class="service-bar-info">
                <span class="service-bar-name">{{ item.nombre }}</span>
                <div class="service-bar-stats">
                  <span class="service-bar-count">{{ item.count }} servicios</span>
                  <span class="service-bar-revenue">{{ fmtCOP(item.total) }}</span>
                </div>
              </div>
              <div class="service-bar-track">
                <div
                  class="service-bar-fill"
                  :style="{ width: (item.total / topServicios[0].total * 100) + '%', background: barColors[i] }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Métodos de pago (donut simple) -->
        <div class="v-card">
          <div class="v-card-header">
            <span class="v-card-title">MÉTODOS DE PAGO</span>
          </div>
          <div class="donut-wrap">
            <div class="donut-svg-wrap">
              <svg viewBox="0 0 160 160">
                <circle
                  v-for="(seg, i) in donutSegments"
                  :key="i"
                  cx="80" cy="80" r="60"
                  fill="none"
                  :stroke="seg.color"
                  stroke-width="18"
                  :stroke-dasharray="`${seg.dash} ${seg.gap}`"
                  :stroke-dashoffset="-seg.offset"
                />
              </svg>
              <div class="donut-center">
                <div class="donut-center-value">{{ fmtCOP(totalVentas) }}</div>
                <div class="donut-center-label">TOTAL</div>
              </div>
            </div>
            <div class="donut-legend">
              <div v-for="(seg, i) in donutSegments" :key="i" class="donut-legend-item">
                <div class="donut-legend-left">
                  <div class="donut-dot" :style="{ background: seg.color }"></div>
                  <span class="donut-legend-name">{{ seg.name }}</span>
                </div>
                <span class="donut-legend-pct">{{ (seg.pct * 100).toFixed(0) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Ventas recientes -->
      <div class="v-card">
        <div class="v-card-header">
          <span class="v-card-title">VENTAS RECIENTES</span>
        </div>
        <table class="recent-sales-table">
          <thead>
            <tr><th>CLIENTE</th><th>SERVICIO</th><th>FECHA</th><th>MONTO</th><th>PAGO</th></tr>
          </thead>
          <tbody>
            <tr v-for="(v, i) in ventas.slice(0, 8)" :key="i">
              <td>{{ v.cliente }}</td>
              <td>{{ v.servicio }}</td>
              <td>{{ formatFecha(v.fecha) }}</td>
              <td><span class="sale-amount">{{ fmtCOP(v.monto) }}</span></td>
              <td><span class="metodo-badge">{{ v.metodo }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ===== SECCIÓN SERVICIOS ===== -->
    <div v-if="activeTab === 'servicios'" class="panel-section">
      <!-- Filtros -->
      <div class="filters-container">
        <div class="filter-tags">
          <button
            v-for="cat in categorias"
            :key="cat"
            class="filter-tag"
            :class="{ active: filtroServicio === cat }"
            @click="filtroServicio = cat"
          >
            {{ cat === 'todos' ? 'Todos' : cat }}
          </button>
        </div>
        <div class="search-and-add">
          <div class="search-box">
            <span><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span>
            <input v-model="searchServicio" type="text" placeholder="Buscar servicio..." />
          </div>
          <button class="btn-red" @click="abrirModalServicio()">+ AGREGAR SERVICIO</button>
        </div>
      </div>

      <div class="result-count">{{ serviciosFiltrados.length }} servicios encontrados</div>

      <div v-if="!serviciosFiltrados.length" class="empty-state">
        <span class="empty-icon"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></span>
        <h3>Sin servicios</h3>
        <p>No hay servicios que coincidan</p>
      </div>

      <div v-else class="services-grid">
        <div
          v-for="s in serviciosFiltrados"
          :key="s.id"
          class="service-card"
        >
          <div class="card-image">
            <img :src="s.imagen" :alt="s.nombre" loading="lazy" />
            <span class="card-badge">{{ s.categoria }}</span>
          </div>
          <div class="card-content">
            <h3>{{ s.nombre }}</h3>
            <p>{{ s.descripcion }}</p>
          </div>
          <div class="card-footer">
            <span class="card-price">${{ s.precio }}</span>
            <span class="card-time"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg> {{ s.duracion }}</span>
          </div>
          <div class="card-actions">
            <button class="btn btn-blue" @click="abrirModalServicio(s)">Editar</button>
            <button class="btn btn-red-outline" @click="eliminarServicio(s.id)">Eliminar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== MODAL CITA ===== -->
    <Teleport to="body">
      <div v-if="modalCita.open" class="modal-backdrop show" @click.self="modalCita.open = false"></div>
      <div v-if="modalCita.open" class="modal open">
        <div class="modal-header">
          <h2>{{ modalCita.editando ? 'EDITAR' : 'NUEVA' }} <span>CITA</span></h2>
          <button class="modal-close" @click="modalCita.open = false"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>CLIENTE <span class="required">*</span></label>
            <input v-model="modalCita.form.cliente" type="text" placeholder="Nombre del cliente" />
          </div>
          <div class="form-group">
            <label>EMAIL</label>
            <input v-model="modalCita.form.email" type="email" placeholder="cliente@email.com" />
          </div>
          <div class="form-group">
            <label>SERVICIO <span class="required">*</span></label>
            <select v-model="modalCita.form.servicio">
              <option value="">Seleccionar servicio…</option>
              <option v-for="s in servicios" :key="s.id">{{ s.nombre }}</option>
            </select>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>FECHA <span class="required">*</span></label>
              <input v-model="modalCita.form.fecha" type="date" />
            </div>
            <div class="form-group">
              <label>HORA <span class="required">*</span></label>
              <input v-model="modalCita.form.hora" type="time" />
            </div>
          </div>
          <div class="form-group">
            <label>ESTADO</label>
            <select v-model="modalCita.form.estado">
              <option value="pendiente">Pendiente</option>
              <option value="confirmada">Confirmada</option>
              <option value="completada">Completada</option>
              <option value="cancelada">Cancelada</option>
            </select>
          </div>
          <button class="btn-full btn-red" @click="guardarCita">
            {{ modalCita.editando ? 'GUARDAR CAMBIOS' : '+ AGREGAR CITA' }}
          </button>
          <button class="btn-full btn-dark" @click="modalCita.open = false">CANCELAR</button>
        </div>
      </div>
    </Teleport>

    <!-- ===== MODAL SERVICIO ===== -->
    <Teleport to="body">
      <div v-if="modalServicio.open" class="modal-backdrop show" @click.self="modalServicio.open = false"></div>
      <div v-if="modalServicio.open" class="modal open">
        <div class="modal-header">
          <h2>{{ modalServicio.editando ? 'EDITAR' : 'NUEVO' }} <span>SERVICIO</span></h2>
          <button class="modal-close" @click="modalServicio.open = false"><svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg></button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>NOMBRE DEL SERVICIO <span class="required">*</span></label>
            <input v-model="modalServicio.form.nombre" type="text" placeholder="Ej: Cambio de Aceite" />
          </div>
          <div class="form-group">
            <label>CATEGORÍA <span class="required">*</span></label>
            <select v-model="modalServicio.form.categoria" class="filter-select w-100" style="width: 100%; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 0.8rem 1rem; color: white; font-family: 'Outfit', sans-serif; border-radius: 4px; outline: none; transition: border-color 0.3s;">
              <option value="" style="background: #1a1a1a; color: white;">Seleccionar categoría…</option>
              <option value="Mantenimiento" style="background: #1a1a1a; color: white;">Mantenimiento</option>
              <option value="Suspensión" style="background: #1a1a1a; color: white;">Suspensión</option>
              <option value="Frenos" style="background: #1a1a1a; color: white;">Frenos</option>
              <option value="Diagnóstico" style="background: #1a1a1a; color: white;">Diagnóstico</option>
              <option value="Eléctrico" style="background: #1a1a1a; color: white;">Eléctrico</option>
              <option value="Confort" style="background: #1a1a1a; color: white;">Confort</option>
              <option value="Transmisión" style="background: #1a1a1a; color: white;">Transmisión</option>
              <option value="Motor" style="background: #1a1a1a; color: white;">Motor</option>
            </select>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>PRECIO ($) <span class="required">*</span></label>
              <input v-model.number="modalServicio.form.precio" type="number" placeholder="0" />
            </div>
            <div class="form-group">
              <label>DURACIÓN <span class="required">*</span></label>
              <input v-model="modalServicio.form.duracion" type="text" placeholder="Ej: 30 min" />
            </div>
          </div>
          <div class="form-group">
            <label>DESCRIPCIÓN</label>
            <textarea v-model="modalServicio.form.descripcion" rows="3" placeholder="Descripción del servicio..."></textarea>
          </div>
          <div class="form-group">
            <label>URL DE IMAGEN</label>
            <input v-model="modalServicio.form.imagen" type="url" placeholder="https://..." />
          </div>
          <button class="btn-full btn-red" @click="guardarServicio">
            {{ modalServicio.editando ? 'GUARDAR CAMBIOS' : '+ AGREGAR SERVICIO' }}
          </button>
          <button class="btn-full btn-dark" @click="modalServicio.open = false">CANCELAR</button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

// ==================== TABS ====================
const tabs = [
  { id: 'citas', label: 'Citas', icon: '<svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>' },
  { id: 'ventas', label: 'Ventas', icon: '<svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>' },
  { id: 'servicios', label: 'Servicios', icon: '<svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/></svg>' },
]
const activeTab = ref('citas')

// ==================== SERVICIOS (datos) ====================
const IMAGENES_CAT = {
  'Mantenimiento': 'https://images.unsplash.com/photo-1612836691696-6a8b5b4e0b70?w=400',
  'Suspensión':    'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=400',
  'Frenos':        'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=400',
  'Diagnóstico':   'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400',
  'Eléctrico':     'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
  'Confort':       'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400',
  'Transmisión':   'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=400',
  'Motor':         'https://images.unsplash.com/photo-1597762470488-3877b1f538c6?w=400',
}

const servicios = ref([
  { id: 1,  nombre: 'Cambio de Aceite',          categoria: 'Mantenimiento', precio: 45,  duracion: '30 min',    descripcion: 'Cambio de aceite y filtro con lubricantes de primera calidad.', imagen: IMAGENES_CAT['Mantenimiento'] },
  { id: 2,  nombre: 'Alineación y Balanceo',      categoria: 'Suspensión',    precio: 60,  duracion: '1 hora',    descripcion: 'Alineación computarizada y balanceo de las 4 ruedas.',          imagen: IMAGENES_CAT['Suspensión'] },
  { id: 3,  nombre: 'Frenos Completos',           categoria: 'Frenos',        precio: 180, duracion: '2 horas',   descripcion: 'Cambio de pastillas, discos y revisión del sistema hidráulico.', imagen: IMAGENES_CAT['Frenos'] },
  { id: 4,  nombre: 'Diagnóstico Computarizado',  categoria: 'Diagnóstico',   precio: 50,  duracion: '45 min',    descripcion: 'Escaneo completo del sistema electrónico con equipo moderno.',   imagen: IMAGENES_CAT['Diagnóstico'] },
  { id: 5,  nombre: 'Cambio de Batería',          categoria: 'Eléctrico',     precio: 120, duracion: '30 min',    descripcion: 'Diagnóstico e instalación de batería nueva con garantía.',        imagen: IMAGENES_CAT['Eléctrico'] },
  { id: 6,  nombre: 'Aire Acondicionado',         categoria: 'Confort',       precio: 90,  duracion: '1 hora',    descripcion: 'Recarga de gas y revisión del sistema de climatización.',          imagen: IMAGENES_CAT['Confort'] },
  { id: 7,  nombre: 'Servicio de Transmisión',    categoria: 'Transmisión',   precio: 150, duracion: '2.5 horas', descripcion: 'Cambio de aceite de caja y revisión del embrague.',               imagen: IMAGENES_CAT['Transmisión'] },
  { id: 8,  nombre: 'Revisión de Motor',          categoria: 'Motor',         precio: 200, duracion: '3 horas',   descripcion: 'Inspección completa: bujías, correa, enfriamiento.',              imagen: IMAGENES_CAT['Motor'] },
  { id: 9,  nombre: 'Lavado Profundo',            categoria: 'Mantenimiento', precio: 35,  duracion: '1.5 horas', descripcion: 'Lavado exterior e interior completo con productos premium.',       imagen: IMAGENES_CAT['Mantenimiento'] },
  { id: 10, nombre: 'Sistema Eléctrico',          categoria: 'Eléctrico',     precio: 80,  duracion: '1 hora',    descripcion: 'Revisión de instalación eléctrica, fusibles y relés.',            imagen: IMAGENES_CAT['Eléctrico'] },
])

const categorias = ['todos', 'Mantenimiento', 'Suspensión', 'Frenos', 'Diagnóstico', 'Eléctrico', 'Confort', 'Transmisión', 'Motor']
const filtroServicio = ref('todos')
const searchServicio = ref('')

const serviciosFiltrados = computed(() => {
  let list = filtroServicio.value === 'todos'
    ? servicios.value
    : servicios.value.filter(s => s.categoria === filtroServicio.value)
  if (searchServicio.value.trim()) {
    const q = searchServicio.value.toLowerCase()
    list = list.filter(s => s.nombre.toLowerCase().includes(q) || s.categoria.toLowerCase().includes(q))
  }
  return [...list].sort((a, b) => a.nombre.localeCompare(b.nombre))
})

// ==================== CITAS ====================
const hoy = new Date()
const manana = new Date(hoy); manana.setDate(manana.getDate() + 1)
const fmt = d => d.toISOString().split('T')[0]

const citas = ref([
  { id: 1, cliente: 'Juan Perez',      email: 'juan@email.com',  servicio: 'Cambio de Aceite',  fecha: fmt(hoy),    hora: '10:00', estado: 'confirmada' },
  { id: 2, cliente: 'Maria Gonzalez',  email: 'maria@email.com', servicio: 'Frenos Completos', fecha: fmt(manana), hora: '14:30', estado: 'pendiente'  },
])

const filtroCitas = ref('todas')
const searchCitas = ref('')
const filtrosCitas = [
  { value: 'todas', label: 'Todas' },
  { value: 'pendiente', label: 'Pendientes' },
  { value: 'confirmada', label: 'Confirmadas' },
  { value: 'completada', label: 'Completadas' },
  { value: 'cancelada', label: 'Canceladas' },
]

const citasFiltradas = computed(() => {
  let list = filtroCitas.value === 'todas' ? citas.value : citas.value.filter(c => c.estado === filtroCitas.value)
  if (searchCitas.value.trim()) {
    const q = searchCitas.value.toLowerCase()
    list = list.filter(c => c.cliente.toLowerCase().includes(q) || c.servicio.toLowerCase().includes(q))
  }
  return [...list].sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
})

const citasPor = estado => citas.value.filter(c => c.estado === estado).length

function cambiarEstado(id, estado) {
  const c = citas.value.find(x => x.id === id)
  if (c) c.estado = estado
}

function eliminarCita(id) {
  if (confirm('¿Eliminar esta cita?')) {
    citas.value = citas.value.filter(c => c.id !== id)
  }
}

function exportarCSV() {
  const headers = ['ID', 'Cliente', 'Email', 'Servicio', 'Fecha', 'Hora', 'Estado']
  const rows = citas.value.map(c => [c.id, c.cliente, c.email || '', c.servicio, c.fecha, c.hora, c.estado])
  const csv = [headers, ...rows].map(r => r.map(x => `"${String(x).replace(/"/g, '""')}"`).join(',')).join('\n')
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' }))
  a.download = `citas_${fmt(new Date())}.csv`
  a.click()
}

// ==================== MODAL CITA ====================
const modalCita = reactive({
  open: false,
  editando: false,
  editId: null,
  form: { cliente: '', email: '', servicio: '', fecha: '', hora: '', estado: 'pendiente' },
})

function abrirModalCita(cita = null) {
  if (cita) {
    modalCita.editando = true
    modalCita.editId = cita.id
    Object.assign(modalCita.form, { ...cita })
  } else {
    modalCita.editando = false
    modalCita.editId = null
    Object.assign(modalCita.form, { cliente: '', email: '', servicio: '', fecha: '', hora: '', estado: 'pendiente' })
  }
  modalCita.open = true
}

function guardarCita() {
  const { cliente, servicio, fecha, hora } = modalCita.form
  if (!cliente || !servicio || !fecha || !hora) { alert('Completa los campos obligatorios'); return }

  if (modalCita.editando) {
    const i = citas.value.findIndex(c => c.id === modalCita.editId)
    if (i !== -1) citas.value[i] = { ...citas.value[i], ...modalCita.form }
  } else {
    citas.value.push({ id: Date.now(), ...modalCita.form })
  }
  modalCita.open = false
}

// ==================== VENTAS ====================
const genVentas = () => {
  const precios = { 'Cambio de Aceite': 45000, 'Alineacion y Balanceo': 60000, 'Frenos Completos': 150000, 'Diagnostico Computarizado': 80000, 'Cambio de Bateria': 120000 }
  const srvs = Object.keys(precios)
  const cls = ['Juan Perez', 'Maria Gonzalez', 'Carlos Ruiz', 'Ana Martinez', 'Luis Hernandez']
  const mets = ['Efectivo', 'Transferencia', 'Tarjeta']
  const result = []
  const now = new Date()
  for (let i = 0; i < 6; i++) {
    const mes = new Date(now.getFullYear(), now.getMonth() - i, 1)
    for (let j = 0; j < 10; j++) {
      const s = srvs[Math.floor(Math.random() * srvs.length)]
      const d = new Date(mes.getFullYear(), mes.getMonth(), Math.floor(Math.random() * 28) + 1)
      result.push({ id: Date.now() - (i * 30 + j) * 86400000 + j, cliente: cls[Math.floor(Math.random() * cls.length)], servicio: s, monto: precios[s] + (Math.floor(Math.random() * 10000) - 5000), fecha: d.toISOString().split('T')[0], metodo: mets[Math.floor(Math.random() * 3)] })
    }
  }
  return result.sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
}

const ventas = ref(genVentas())

const now = new Date()
const ventasMes = computed(() => ventas.value.filter(v => { const d = new Date(v.fecha); return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear() }))
const ventasMesAnterior = computed(() => { const p = new Date(now.getFullYear(), now.getMonth() - 1, 1); return ventas.value.filter(v => { const d = new Date(v.fecha); return d.getMonth() === p.getMonth() && d.getFullYear() === p.getFullYear() }) })
const ingresosMes = computed(() => ventasMes.value.reduce((s, v) => s + v.monto, 0))
const ingresosMesAnt = computed(() => ventasMesAnterior.value.reduce((s, v) => s + v.monto, 0))
const cambioPct = computed(() => ingresosMesAnt.value > 0 ? parseFloat(((ingresosMes.value - ingresosMesAnt.value) / ingresosMesAnt.value * 100).toFixed(1)) : 0)
const ticketPromedio = computed(() => ventasMes.value.length ? Math.round(ingresosMes.value / ventasMes.value.length) : 0)
const topServicio = computed(() => { const c = {}; ventas.value.forEach(v => c[v.servicio] = (c[v.servicio] || 0) + 1); return Object.entries(c).sort((a, b) => b[1] - a[1])[0]?.[0]?.split(' ')[0] || '—' })
const totalVentas = computed(() => ventas.value.reduce((s, v) => s + v.monto, 0))

const datosMensuales = computed(() => {
  return Array.from({ length: 6 }, (_, i) => {
    const d = new Date(now.getFullYear(), now.getMonth() - (5 - i), 1)
    const label = d.toLocaleString('es', { month: 'short' }).toUpperCase().substring(0, 3)
    const total = ventas.value.filter(v => { const vd = new Date(v.fecha); return vd.getMonth() === d.getMonth() && vd.getFullYear() === d.getFullYear() }).reduce((s, v) => s + v.monto, 0)
    return { label, total }
  })
})

const maxBarras = computed(() => Math.max(...datosMensuales.value.map(d => d.total), 1))
const barHeight = total => (total / maxBarras.value * 150).toFixed(1)

const topServicios = computed(() => {
  const bySvc = {}
  ventas.value.forEach(v => { if (!bySvc[v.servicio]) bySvc[v.servicio] = { count: 0, total: 0 }; bySvc[v.servicio].count++; bySvc[v.servicio].total += v.monto })
  return Object.entries(bySvc).sort((a, b) => b[1].total - a[1].total).slice(0, 5).map(([nombre, d]) => ({ nombre, ...d }))
})

const barColors = ['#dc2626', '#2563eb', '#d97706', '#16a34a', '#7c3aed']

const donutSegments = computed(() => {
  const byM = { Efectivo: 0, Transferencia: 0, Tarjeta: 0 }
  const colors = { Efectivo: '#dc2626', Transferencia: '#2563eb', Tarjeta: '#16a34a' }
  ventas.value.forEach(v => byM[v.metodo] = (byM[v.metodo] || 0) + v.monto)
  const total = Object.values(byM).reduce((s, v) => s + v, 0)
  const circ = 2 * Math.PI * 60
  let offset = 0
  return Object.entries(byM).map(([name, val]) => {
    const pct = val / total
    const seg = { name, pct, color: colors[name], dash: circ * pct, gap: circ - circ * pct, offset }
    offset += circ * pct
    return seg
  })
})

// Venta rápida
const qsCliente = ref('')
const qsServicio = ref('')
const qsMetodo = ref('Efectivo')
const qsMonto = ref(0)

function autoFillPrecio() {
  const s = servicios.value.find(x => x.nombre === qsServicio.value)
  if (s) qsMonto.value = s.precio
}

function registrarVenta() {
  if (!qsCliente.value || !qsServicio.value || !qsMonto.value) { alert('Completa todos los campos'); return }
  ventas.value.unshift({ id: Date.now(), cliente: qsCliente.value, servicio: qsServicio.value, monto: qsMonto.value, fecha: fmt(new Date()), metodo: qsMetodo.value })
  qsCliente.value = ''; qsServicio.value = ''; qsMonto.value = 0
}

// ==================== MODAL SERVICIO ====================
const modalServicio = reactive({
  open: false,
  editando: false,
  editId: null,
  form: { nombre: '', categoria: '', precio: 0, duracion: '', descripcion: '', imagen: '' },
})

function abrirModalServicio(serv = null) {
  if (serv) {
    modalServicio.editando = true
    modalServicio.editId = serv.id
    Object.assign(modalServicio.form, { ...serv })
  } else {
    modalServicio.editando = false
    modalServicio.editId = null
    Object.assign(modalServicio.form, { nombre: '', categoria: '', precio: 0, duracion: '', descripcion: '', imagen: '' })
  }
  modalServicio.open = true
}

function guardarServicio() {
  const { nombre, categoria, precio, duracion } = modalServicio.form
  if (!nombre || !categoria || !precio || !duracion) { alert('Completa los campos obligatorios'); return }
  const imagen = modalServicio.form.imagen || IMAGENES_CAT[categoria] || ''

  if (modalServicio.editando) {
    const i = servicios.value.findIndex(s => s.id === modalServicio.editId)
    if (i !== -1) servicios.value[i] = { ...servicios.value[i], ...modalServicio.form, imagen }
  } else {
    servicios.value.push({ id: Date.now(), ...modalServicio.form, imagen })
  }
  modalServicio.open = false
}

function eliminarServicio(id) {
  if (confirm('¿Eliminar este servicio?')) {
    servicios.value = servicios.value.filter(s => s.id !== id)
  }
}

// ==================== UTILS ====================
/**
 * Formatea una fecha YYYY-MM-DD a representación localizada en español.
 * @param {string} fecha - Cadena de fecha en formato ISO/YYYY-MM-DD
 * @returns {string} Fecha formateada en español
 */
function formatFecha(fecha) {
  return new Date(fecha + 'T12:00:00').toLocaleDateString('es')
}

/**
 * Formatea un monto numérico a moneda COP abreviada.
 * @param {number} n - Monto numérico
 * @returns {string} Cadena formateada
 */
function fmtCOP(n) {
  if (n >= 1000000) return '$' + (n / 1000000).toFixed(1) + 'M'
  if (n >= 1000) return '$' + (n / 1000).toFixed(0) + 'K'
  return '$' + n
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Montserrat:wght@700;800;900&display=swap');

/* ===== VARIABLES ===== */
.admin-wrapper {
  --primary: #dc2626;
  --primary-dark: #b91c1c;
  --primary-glow: rgba(220, 38, 38, 0.25);
  --bg-deep: #000000;
  --bg-base: #0a0a0a;
  --bg-card: #111111;
  --bg-lift: #1a1a1a;
  --text-primary: #ffffff;
  --text-secondary: #a0a0a0;
  --text-muted: #6b6b6b;
  --border-light: rgba(255,255,255,0.08);
  --border-red: rgba(220,38,38,0.2);
  --shadow-red: 0 4px 20px rgba(220,38,38,0.25);
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;

  font-family: 'Inter', sans-serif;
  background: var(--bg-base);
  color: var(--text-primary);
  min-height: unset;
}

/* ===== TABS ===== */
.panel-tabs {
  display: flex;
  gap: 0.25rem;
  padding: 0.75rem 1.5rem 0;
  border-bottom: 1px solid var(--border-red);
  background: var(--bg-deep);
}

.panel-tab {
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 8px 8px 0 0;
  position: relative;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}
.panel-tab:hover { color: white; background: rgba(220,38,38,0.08); }
.panel-tab.active {
  color: white;
  background: rgba(220,38,38,0.12);
}
.panel-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0; right: 0;
  height: 2px;
  background: var(--primary);
}

/* ===== PANEL SECTION ===== */
.panel-section { padding: 2rem; }

/* ===== STATS ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.25rem;
  transition: all 0.25s ease;
}
.stat-card:hover { transform: translateY(-3px); border-color: var(--border-red); }
.stat-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; }
.stat-number { font-size: 2rem; font-weight: 800; line-height: 1; }
.stat-number.white { color: white; }
.stat-number.yellow { color: #fbbf24; }
.stat-number.blue { color: #60a5fa; }
.stat-number.green { color: #34d399; }
.stat-number.red { color: #f87171; }
.stat-icon { font-size: 1.5rem; opacity: 0.25; }
.stat-label { color: var(--text-secondary); font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.5rem; }
.stat-bar { height: 3px; border-radius: 2px; width: 100%; }

/* ===== TOOLBAR ===== */
.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}
.filter-tags { display: flex; gap: 0.4rem; flex-wrap: wrap; }
.filter-tag {
  padding: 0.4rem 0.9rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}
.filter-tag:hover { color: white; border-color: var(--border-red); }
.filter-tag.active { background: var(--primary); color: white; border-color: var(--primary); }

.toolbar-actions { display: flex; gap: 0.75rem; align-items: center; }
.search-input {
  padding: 0.5rem 0.9rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: white;
  font-size: 0.85rem;
  outline: none;
  min-width: 220px;
  font-family: 'Inter', sans-serif;
  transition: border-color 0.2s ease;
}
.search-input:focus { border-color: var(--primary); }

/* ===== BOTONES ===== */
.btn-red {
  padding: 0.55rem 1.2rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: 'Inter', sans-serif;
  letter-spacing: 0.5px;
}
.btn-red:hover { background: var(--primary-dark); transform: translateY(-1px); box-shadow: var(--shadow-red); }

.btn-ghost {
  padding: 0.55rem 1.2rem;
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: 'Inter', sans-serif;
}
.btn-ghost:hover { color: white; border-color: var(--primary); }

/* ===== TABLA ===== */
.table-container {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  overflow: hidden;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th {
  padding: 0.85rem 1rem;
  text-align: left;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--text-muted);
  background: rgba(255,255,255,0.02);
  border-bottom: 1px solid var(--border-light);
}
.table td {
  padding: 0.9rem 1rem;
  border-bottom: 1px solid var(--border-light);
  font-size: 0.88rem;
}
.table tbody tr:last-child td { border-bottom: none; }
.table tbody tr { transition: background 0.15s ease; }
.table tbody tr:hover { background: rgba(220,38,38,0.03); }

.cliente-cell { display: flex; align-items: center; gap: 0.75rem; }
.avatar {
  width: 34px; height: 34px;
  background: var(--primary);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 0.9rem;
  flex-shrink: 0;
}
.cliente-nombre { font-weight: 600; }
.cliente-email { font-size: 0.75rem; color: var(--text-muted); }

.acciones-cell { display: flex; gap: 0.5rem; align-items: center; }
.status-select {
  padding: 0.3rem 0.6rem;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--border-light);
  border-radius: 6px;
  color: white;
  font-size: 0.78rem;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
}
.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.25rem;
  border-radius: 6px;
  transition: transform 0.15s ease;
}
.action-btn:hover { transform: scale(1.2); }

/* BADGES */
.badge {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  border: 1px solid transparent;
}
.badge-pendiente  { background: rgba(245,158,11,.12); color: #fbbf24; border-color: rgba(245,158,11,.3); }
.badge-confirmada { background: rgba(59,130,246,.12);  color: #93c5fd; border-color: rgba(59,130,246,.3);  }
.badge-completada { background: rgba(16,185,129,.12);  color: #6ee7b7; border-color: rgba(16,185,129,.3);  }
.badge-cancelada  { background: rgba(220,38,38,.12);   color: #fca5a5; border-color: rgba(220,38,38,.3);   }

/* EMPTY STATE */
.empty-state {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; padding: 5rem 2rem; text-align: center;
}
.empty-icon { font-size: 3rem; opacity: 0.3; margin-bottom: 1rem; }
.empty-state h3 {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.2rem; font-weight: 800;
  text-transform: uppercase; letter-spacing: 1px;
  color: rgba(255,255,255,.25); margin-bottom: 0.5rem;
}
.empty-state p { font-size: 0.85rem; color: rgba(255,255,255,.18); margin-bottom: 1.5rem; }

/* ===== VENTAS STATS ===== */
.ventas-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.venta-stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
  transition: transform 0.25s ease;
}
.venta-stat-card:hover { transform: translateY(-3px); border-color: var(--border-red); }
.venta-stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
}
.venta-stat-card.rojo::before    { background: linear-gradient(90deg,#dc2626,#f87171); }
.venta-stat-card.verde::before   { background: linear-gradient(90deg,#16a34a,#4ade80); }
.venta-stat-card.azul::before    { background: linear-gradient(90deg,#2563eb,#60a5fa); }
.venta-stat-card.amarillo::before { background: linear-gradient(90deg,#d97706,#fbbf24); }
.vs-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.vs-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem; }
.vs-value { font-size: 1.8rem; font-weight: 800; color: white; margin-bottom: 0.25rem; }
.vs-change { font-size: 0.75rem; font-weight: 600; }
.vs-change.pos { color: #4ade80; }
.vs-change.neg { color: #f87171; }
.vs-sub { font-size: 0.75rem; color: var(--text-muted); }

/* ===== V-CARDS ===== */
.ventas-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
.v-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
}
.v-card-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 1.25rem;
}
.v-card-title { font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-secondary); }
.v-card-badge { font-size: 0.68rem; padding: 0.2rem 0.6rem; background: rgba(220,38,38,.1); color: var(--primary); border-radius: 20px; border: 1px solid var(--border-red); }

/* Barras mensuales */
.bar-chart-wrap {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  height: 170px;
  padding-bottom: 0.25rem;
}
.bar-col { display: flex; flex-direction: column; align-items: center; flex: 1; gap: 0.3rem; }
.bar-fill {
  width: 100%;
  background: rgba(220,38,38,.35);
  border-radius: 4px 4px 0 0;
  position: relative;
  min-height: 4px;
  transition: height 0.6s cubic-bezier(.22,1,.36,1);
  cursor: default;
}
.bar-fill.highlight { background: var(--primary); }
.bar-fill:hover .bar-tooltip { opacity: 1; }
.bar-tooltip {
  position: absolute;
  top: -28px;
  left: 50%; transform: translateX(-50%);
  background: #222; color: white;
  font-size: 0.68rem; padding: 0.2rem 0.4rem;
  border-radius: 4px; white-space: nowrap;
  opacity: 0; pointer-events: none;
  transition: opacity 0.15s ease;
}
.bar-label { font-size: 0.65rem; color: var(--text-muted); font-weight: 600; }

/* Quick sale */
.quick-sale-form { display: flex; flex-direction: column; gap: 0.75rem; }
.qs-group { display: flex; flex-direction: column; gap: 0.3rem; }
.qs-group label { font-size: 0.68rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: var(--text-muted); }
.qs-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.qs-input {
  padding: 0.55rem 0.8rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: white;
  font-size: 0.88rem;
  outline: none;
  font-family: 'Inter', sans-serif;
  transition: border-color 0.2s ease;
}
.qs-input:focus { border-color: var(--primary); }
.qs-total {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.75rem; background: rgba(220,38,38,.06);
  border: 1px solid var(--border-red); border-radius: 8px;
}
.qs-total-label { font-size: 0.78rem; color: var(--text-secondary); font-weight: 600; }
.qs-total-value { font-size: 1.3rem; font-weight: 800; color: var(--primary); }
.btn-full { width: 100%; padding: 0.75rem; border: none; border-radius: 8px; font-size: 0.85rem; font-weight: 700; cursor: pointer; font-family: 'Inter', sans-serif; letter-spacing: 0.5px; }

/* Service bars */
.service-bars { display: flex; flex-direction: column; gap: 1rem; }
.service-bar-item { display: flex; flex-direction: column; gap: 0.4rem; }
.service-bar-info { display: flex; justify-content: space-between; align-items: flex-start; }
.service-bar-name { font-size: 0.82rem; font-weight: 600; }
.service-bar-stats { display: flex; gap: 0.75rem; }
.service-bar-count { font-size: 0.72rem; color: var(--text-muted); }
.service-bar-revenue { font-size: 0.78rem; color: var(--primary); font-weight: 700; }
.service-bar-track { height: 5px; background: rgba(255,255,255,.06); border-radius: 3px; overflow: hidden; }
.service-bar-fill { height: 100%; border-radius: 3px; transition: width 0.7s cubic-bezier(.22,1,.36,1); }

/* Donut */
.donut-wrap { display: flex; align-items: center; gap: 2rem; }
.donut-svg-wrap { position: relative; width: 160px; height: 160px; flex-shrink: 0; }
.donut-svg-wrap svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.donut-center {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.donut-center-value { font-size: 1rem; font-weight: 800; color: white; }
.donut-center-label { font-size: 0.6rem; color: var(--text-muted); letter-spacing: 1px; text-transform: uppercase; }
.donut-legend { display: flex; flex-direction: column; gap: 0.6rem; }
.donut-legend-item { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.donut-legend-left { display: flex; align-items: center; gap: 0.5rem; }
.donut-dot { width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; }
.donut-legend-name { font-size: 0.8rem; color: var(--text-secondary); }
.donut-legend-pct { font-size: 0.8rem; font-weight: 700; color: white; }

/* Recent sales table */
.recent-sales-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.recent-sales-table th { padding: 0.5rem 0.75rem; font-size: 0.65rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-muted); border-bottom: 1px solid var(--border-light); }
.recent-sales-table td { padding: 0.65rem 0.75rem; border-bottom: 1px solid rgba(255,255,255,.04); }
.sale-amount { color: var(--primary); font-weight: 700; }
.metodo-badge { font-size: 0.72rem; padding: 0.2rem 0.6rem; border-radius: 12px; background: rgba(255,255,255,.06); color: var(--text-secondary); }

/* ===== SERVICIOS GRID ===== */
.filters-container {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;
}
.search-and-add { display: flex; gap: 0.75rem; align-items: center; }
.search-box {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.5rem 0.8rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-light);
  border-radius: 8px;
}
.search-box input {
  background: transparent; border: none; outline: none;
  color: white; font-size: 0.85rem; font-family: 'Inter', sans-serif;
  min-width: 180px;
}

.result-count { font-size: 0.78rem; color: var(--text-muted); margin-bottom: 1.5rem; }

.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
.service-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.25s ease;
}
.service-card:hover { transform: translateY(-5px); border-color: var(--border-red); box-shadow: 0 10px 30px rgba(220,38,38,.1); }
.card-image { height: 160px; position: relative; overflow: hidden; }
.card-image img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.service-card:hover .card-image img { transform: scale(1.08); }
.card-badge {
  position: absolute; bottom: 8px; left: 8px;
  background: rgba(0,0,0,.8); color: var(--primary);
  padding: 0.25rem 0.6rem; border-radius: 4px;
  font-size: 0.65rem; font-weight: 700;
  border: 1px solid var(--border-red);
}
.card-content { padding: 1rem 1rem 0.5rem; }
.card-content h3 { font-size: 0.95rem; font-weight: 700; margin-bottom: 0.4rem; }
.card-content p { color: var(--text-secondary); font-size: 0.8rem; line-height: 1.6; }
.card-footer {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.75rem 1rem;
}
.card-price { font-size: 1.3rem; font-weight: 800; color: var(--primary); }
.card-time { font-size: 0.75rem; color: var(--text-muted); }
.card-actions {
  display: flex; gap: 0.5rem; padding: 0.75rem 1rem;
  border-top: 1px solid var(--border-light);
}
.btn { padding: 0.4rem 0.9rem; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer; font-family: 'Inter', sans-serif; border: none; transition: all 0.2s ease; }
.btn-blue { background: rgba(59,130,246,.15); color: #93c5fd; border: 1px solid rgba(59,130,246,.3); }
.btn-blue:hover { background: rgba(59,130,246,.3); }
.btn-red-outline { background: rgba(220,38,38,.1); color: #fca5a5; border: 1px solid rgba(220,38,38,.3); }
.btn-red-outline:hover { background: rgba(220,38,38,.25); }

/* ===== MODAL ===== */
.modal-backdrop {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.85);
  backdrop-filter: blur(10px);
  z-index: 9000;
}
.modal {
  position: fixed; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9001;
  width: min(90vw, 460px);
  background: #111;
  border: 1px solid rgba(220,38,38,.25);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 30px 70px rgba(0,0,0,.7);
}
.modal::before { content: ''; display: block; height: 2px; background: linear-gradient(90deg, transparent, #dc2626, transparent); }
.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.5rem 1.75rem 0;
}
.modal-header h2 { font-family: 'Montserrat', sans-serif; font-size: 1.4rem; font-weight: 900; letter-spacing: 1px; }
.modal-header h2 span { color: var(--primary); }
.modal-close {
  width: 32px; height: 32px;
  border-radius: 8px; border: 1px solid rgba(255,255,255,.1);
  background: rgba(255,255,255,.05); color: #777;
  font-size: 0.9rem; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.2s ease; font-family: 'Inter', sans-serif;
}
.modal-close:hover { background: var(--primary); color: white; transform: rotate(90deg); }
.modal-body { padding: 1.25rem 1.75rem 1.75rem; display: flex; flex-direction: column; gap: 0.85rem; max-height: 70vh; overflow-y: auto; scrollbar-width: thin; scrollbar-color: #dc2626 transparent; }
.form-group { display: flex; flex-direction: column; gap: 0.35rem; }
.form-group label { font-size: 0.67rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-muted); }
.required { color: var(--primary); }
.form-group input, .form-group select, .form-group textarea {
  padding: 0.65rem 0.85rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: white;
  font-size: 0.88rem;
  outline: none;
  font-family: 'Inter', sans-serif;
  transition: border-color 0.2s ease;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: var(--primary); background: rgba(220,38,38,.04); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.btn-full.btn-red { background: var(--primary); color: white; box-shadow: 0 4px 18px rgba(220,38,38,.3); }
.btn-full.btn-red:hover { background: var(--primary-dark); transform: translateY(-1px); }
.btn-full.btn-dark { background: rgba(255,255,255,.06); color: var(--text-secondary); border: 1px solid var(--border-light); }
.btn-full.btn-dark:hover { color: white; border-color: var(--border-red); }

/* ===== RESPONSIVE ===== */
@media (max-width: 1200px) {
  .stats-grid { grid-template-columns: repeat(3, 1fr); }
  .ventas-stats { grid-template-columns: repeat(2, 1fr); }
  .services-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .panel-section { padding: 1rem; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .ventas-grid { grid-template-columns: 1fr; }
  .services-grid { grid-template-columns: 1fr; }
  .table-toolbar { flex-direction: column; align-items: flex-start; }
  .toolbar-actions { flex-wrap: wrap; }
}
</style>
