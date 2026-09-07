"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { ProyectoInversion, ContratoSeguimiento, PresupuestoProyecto } from "@/types";
import { formatCurrency, getEstadoBadgeClass } from "@/lib/utils";
import Modal from "@/components/Modal";
import { Plus, Briefcase, FileText, DollarSign, Edit, Trash2, ExternalLink } from "lucide-react";

export default function EjecucionPage() {
  const { token } = useAuth();
  const [tab, setTab] = useState<"proyectos" | "contratos" | "presupuesto">("proyectos");
  const [loading, setLoading] = useState(true);

  const [proyectos, setProyectos] = useState<ProyectoInversion[]>([]);
  const [contratos, setContratos] = useState<ContratoSeguimiento[]>([]);
  const [presupuestos, setPresupuestos] = useState<(PresupuestoProyecto & { proyecto_nombre?: string })[]>([]);

  const [showProyectoForm, setShowProyectoForm] = useState(false);
  const [editProyecto, setEditProyecto] = useState<ProyectoInversion | null>(null);
  const [proyectoForm, setProyectoForm] = useState({ codigo_interno: "", codigo_bpin: "", nombre: "", objetivo: "", dependencia_id: "", vigencia_inicio: 2024, vigencia_fin: 2027, estado: "FORMULACION", fuente_origen: "" });

  const [showContratoForm, setShowContratoForm] = useState(false);
  const [editContrato, setEditContrato] = useState<ContratoSeguimiento | null>(null);
  const [contratoForm, setContratoForm] = useState({ numero: "", secop_id: "", objeto: "", contratista: "", valor_inicial: 0, valor_actual: 0, estado: "EN_EJECUCION" });
  const [selectedProyectoId, setSelectedProyectoId] = useState<string>("");

  const [showPresupuestoForm, setShowPresupuestoForm] = useState(false);
  const [editPresupuesto, setEditPresupuesto] = useState<PresupuestoProyecto | null>(null);
  const [presupuestoForm, setPresupuestoForm] = useState({ vigencia: 2024, fuente: "", apropiacion_inicial: 0, adiciones: 0, reducciones: 0, apropiacion_definitiva: 0 });
  const [selectedProyectoPresupuesto, setSelectedProyectoPresupuesto] = useState<string>("");

  const loadProyectos = useCallback(async () => {
    if (!token) return;
    const data = await api.get<ProyectoInversion[]>("/planeacion/proyectos", token);
    setProyectos(data);
  }, [token]);

  const loadContratos = useCallback(async () => {
    if (!token) return;
    const all: ContratoSeguimiento[] = [];
    for (const p of proyectos) {
      try {
        const cs = await api.get<ContratoSeguimiento[]>(`/planeacion/proyectos/${p.id}/contratos`, token);
        all.push(...cs);
      } catch {}
    }
    setContratos(all);
  }, [token, proyectos]);

  const loadPresupuestos = useCallback(async () => {
    if (!token) return;
    const all: (PresupuestoProyecto & { proyecto_nombre?: string })[] = [];
    for (const p of proyectos) {
      try {
        const ps = await api.get<PresupuestoProyecto[]>(`/planeacion/proyectos/${p.id}/presupuestos`, token);
        ps.forEach(pr => all.push({ ...pr, proyecto_nombre: p.nombre }));
      } catch {}
    }
    setPresupuestos(all);
  }, [token, proyectos]);

  useEffect(() => { loadProyectos().finally(() => setLoading(false)); }, [loadProyectos]);
  useEffect(() => { if (tab === "contratos" && proyectos.length) loadContratos(); }, [tab, proyectos, loadContratos]);
  useEffect(() => { if (tab === "presupuesto" && proyectos.length) loadPresupuestos(); }, [tab, proyectos, loadPresupuestos]);

  // ─── Proyecto CRUD ───
  const saveProyecto = async () => {
    if (!token) return;
    if (editProyecto) {
      await api.patch(`/planeacion/proyectos/${editProyecto.id}`, proyectoForm, token);
    } else {
      await api.post("/planeacion/proyectos", proyectoForm, token);
    }
    setShowProyectoForm(false);
    setEditProyecto(null);
    loadProyectos();
  };

  const deleteProyecto = async (id: string) => {
    if (!confirm("¿Eliminar este proyecto?")) return;
    await api.delete(`/planeacion/proyectos/${id}`, token!);
    loadProyectos();
  };

  // ─── Contrato CRUD ───
  const saveContrato = async () => {
    if (!token || !selectedProyectoId) return;
    if (editContrato) {
      await api.patch(`/planeacion/contratos/${editContrato.id}`, contratoForm, token);
    } else {
      await api.post(`/planeacion/proyectos/${selectedProyectoId}/contratos`, contratoForm, token);
    }
    setShowContratoForm(false);
    setEditContrato(null);
    setSelectedProyectoId("");
    loadContratos();
  };

  const deleteContrato = async (id: string) => {
    if (!confirm("¿Eliminar este contrato?")) return;
    await api.delete(`/planeacion/contratos/${id}`, token!);
    loadContratos();
  };

  // ─── Presupuesto CRUD ───
  const savePresupuesto = async () => {
    if (!token || !selectedProyectoPresupuesto) return;
    if (editPresupuesto) {
      await api.patch(`/planeacion/presupuestos/${editPresupuesto.id}`, presupuestoForm, token);
    } else {
      await api.post(`/planeacion/proyectos/${selectedProyectoPresupuesto}/presupuestos`, presupuestoForm, token);
    }
    setShowPresupuestoForm(false);
    setEditPresupuesto(null);
    setSelectedProyectoPresupuesto("");
    loadPresupuestos();
  };

  const deletePresupuesto = async (id: string) => {
    if (!confirm("¿Eliminar este presupuesto?")) return;
    await api.delete(`/planeacion/presupuestos/${id}`, token!);
    loadPresupuestos();
  };

  if (loading) {
    return <div className="space-y-4">{[...Array(3)].map((_, i) => <div key={i} className="h-24 bg-gray-100 rounded-xl animate-pulse" />)}</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 border-b border-gray-200 pb-2">
        {([["proyectos", "Proyectos", Briefcase], ["contratos", "Contratos", FileText], ["presupuesto", "Presupuesto", DollarSign]] as const).map(([id, label, Icon]) => (
          <button key={id} onClick={() => setTab(id)} className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-t-lg ${tab === id ? "bg-primary-50 text-primary-700 border-b-2 border-primary-600" : "text-gray-500"}`}>
            <Icon className="h-4 w-4" />{label}
          </button>
        ))}
      </div>

      {/* ─── PROYECTOS ─── */}
      {tab === "proyectos" && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <button onClick={() => { setEditProyecto(null); setProyectoForm({ codigo_interno: "", codigo_bpin: "", nombre: "", objetivo: "", dependencia_id: "", vigencia_inicio: 2024, vigencia_fin: 2027, estado: "FORMULACION", fuente_origen: "" }); setShowProyectoForm(true); }} className="btn-primary flex items-center gap-2"><Plus className="h-4 w-4" /> Nuevo Proyecto</button>
          </div>
          {proyectos.length === 0 ? (
            <div className="card p-12 text-center"><Briefcase className="mx-auto h-12 w-12 text-gray-300" /><p className="mt-4 text-gray-500">No hay proyectos</p></div>
          ) : (
            <div className="space-y-3">
              {proyectos.map(proj => (
                <div key={proj.id} className="card p-5 hover:shadow-md transition-shadow group">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <h3 className="font-semibold text-gray-900">{proj.nombre}</h3>
                        <span className={`badge ${getEstadoBadgeClass(proj.estado)}`}>{proj.estado}</span>
                      </div>
                      <p className="mt-1 text-sm text-gray-500">{proj.codigo_interno} | Vigencia: {proj.vigencia_inicio}-{proj.vigencia_fin}</p>
                      {proj.codigo_bpin && <p className="text-xs text-gray-400 mt-1">BPIN: {proj.codigo_bpin}</p>}
                      {proj.objetivo && <p className="text-sm text-gray-600 mt-2 line-clamp-2">{proj.objetivo}</p>}
                    </div>
                    <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button onClick={() => { setEditProyecto(proj); setProyectoForm({ codigo_interno: proj.codigo_interno, codigo_bpin: proj.codigo_bpin || "", nombre: proj.nombre, objetivo: proj.objetivo || "", dependencia_id: proj.dependencia_id, vigencia_inicio: proj.vigencia_inicio, vigencia_fin: proj.vigencia_fin, estado: proj.estado, fuente_origen: proj.fuente_origen || "" }); setShowProyectoForm(true); }} className="p-2 hover:bg-gray-100 rounded-lg"><Edit className="h-4 w-4 text-gray-500" /></button>
                      <button onClick={() => deleteProyecto(proj.id)} className="p-2 hover:bg-red-50 rounded-lg"><Trash2 className="h-4 w-4 text-red-500" /></button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ─── CONTRATOS ─── */}
      {tab === "contratos" && (
        <div className="space-y-4">
          <div className="flex justify-end gap-2">
            <select className="input w-64" value={selectedProyectoId} onChange={e => setSelectedProyectoId(e.target.value)}>
              <option value="">Seleccionar proyecto...</option>
              {proyectos.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
            </select>
            <button disabled={!selectedProyectoId} onClick={() => { setEditContrato(null); setContratoForm({ numero: "", secop_id: "", objeto: "", contratista: "", valor_inicial: 0, valor_actual: 0, estado: "EN_EJECUCION" }); setShowContratoForm(true); }} className="btn-primary flex items-center gap-2 disabled:opacity-50"><Plus className="h-4 w-4" /> Nuevo Contrato</button>
          </div>
          {contratos.length === 0 ? (
            <div className="card p-12 text-center"><FileText className="mx-auto h-12 w-12 text-gray-300" /><p className="mt-4 text-gray-500">No hay contratos</p></div>
          ) : (
            <div className="card overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Número</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contratista</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Objeto</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Valor</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Avance</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                    <th className="px-4 py-3" />
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {contratos.map(c => (
                    <tr key={c.id} className="hover:bg-gray-50 group">
                      <td className="px-4 py-3 text-sm font-mono text-gray-900">{c.numero}</td>
                      <td className="px-4 py-3 text-sm text-gray-900">{c.contratista}</td>
                      <td className="px-4 py-3 text-sm text-gray-600 max-w-xs truncate">{c.objeto}</td>
                      <td className="px-4 py-3 text-sm text-gray-900">{formatCurrency(c.valor_actual)}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{c.avance_fisico ?? 0}%</td>
                      <td className="px-4 py-3"><span className={`badge ${getEstadoBadgeClass(c.estado)}`}>{c.estado}</span></td>
                      <td className="px-4 py-3 text-right hidden group-hover:table-cell">
                        <button onClick={() => { setEditContrato(c); setContratoForm({ numero: c.numero, secop_id: c.secop_id || "", objeto: c.objeto, contratista: c.contratista, valor_inicial: c.valor_inicial, valor_actual: c.valor_actual, estado: c.estado }); setShowContratoForm(true); }} className="p-1 hover:bg-gray-200 rounded"><Edit className="h-3.5 w-3.5" /></button>
                        <button onClick={() => deleteContrato(c.id)} className="p-1 hover:bg-red-100 rounded text-red-600"><Trash2 className="h-3.5 w-3.5" /></button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* ─── PRESUPUESTO ─── */}
      {tab === "presupuesto" && (
        <div className="space-y-4">
          <div className="flex justify-end gap-2">
            <select className="input w-64" value={selectedProyectoPresupuesto} onChange={e => setSelectedProyectoPresupuesto(e.target.value)}>
              <option value="">Seleccionar proyecto...</option>
              {proyectos.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
            </select>
            <button disabled={!selectedProyectoPresupuesto} onClick={() => { setEditPresupuesto(null); setPresupuestoForm({ vigencia: 2024, fuente: "", apropiacion_inicial: 0, adiciones: 0, reducciones: 0, apropiacion_definitiva: 0 }); setShowPresupuestoForm(true); }} className="btn-primary flex items-center gap-2 disabled:opacity-50"><Plus className="h-4 w-4" /> Nuevo Presupuesto</button>
          </div>
          {presupuestos.length === 0 ? (
            <div className="card p-12 text-center"><DollarSign className="mx-auto h-12 w-12 text-gray-300" /><p className="mt-4 text-gray-500">No hay presupuestos</p></div>
          ) : (
            <div className="card overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Proyecto</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vigencia</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fuente</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Inicial</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Definitiva</th>
                    <th className="px-4 py-3" />
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {presupuestos.map(p => (
                    <tr key={p.id} className="hover:bg-gray-50 group">
                      <td className="px-4 py-3 text-sm text-gray-900">{p.proyecto_nombre}</td>
                      <td className="px-4 py-3 text-sm text-gray-900">{p.vigencia}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{p.fuente}</td>
                      <td className="px-4 py-3 text-sm text-gray-900">{formatCurrency(p.apropiacion_inicial)}</td>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">{formatCurrency(p.apropiacion_definitiva)}</td>
                      <td className="px-4 py-3 text-right hidden group-hover:table-cell">
                        <button onClick={() => { setEditPresupuesto(p); setPresupuestoForm({ vigencia: p.vigencia, fuente: p.fuente, apropiacion_inicial: p.apropiacion_inicial, adiciones: p.adiciones, reducciones: p.reducciones, apropiacion_definitiva: p.apropiacion_definitiva }); setShowPresupuestoForm(true); }} className="p-1 hover:bg-gray-200 rounded"><Edit className="h-3.5 w-3.5" /></button>
                        <button onClick={() => deletePresupuesto(p.id)} className="p-1 hover:bg-red-100 rounded text-red-600"><Trash2 className="h-3.5 w-3.5" /></button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* ─── MODALS ─── */}
      <Modal isOpen={showProyectoForm} onClose={() => { setShowProyectoForm(false); setEditProyecto(null); }} title={editProyecto ? "Editar Proyecto" : "Nuevo Proyecto"}>
        <div className="space-y-4">
          <div><label className="label">Nombre</label><input className="input" value={proyectoForm.nombre} onChange={e => setProyectoForm({...proyectoForm, nombre: e.target.value})} /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Código Interno</label><input className="input" value={proyectoForm.codigo_interno} onChange={e => setProyectoForm({...proyectoForm, codigo_interno: e.target.value})} /></div>
            <div><label className="label">BPIN</label><input className="input" value={proyectoForm.codigo_bpin} onChange={e => setProyectoForm({...proyectoForm, codigo_bpin: e.target.value})} /></div>
          </div>
          <div><label className="label">Objetivo</label><textarea className="input" rows={2} value={proyectoForm.objetivo} onChange={e => setProyectoForm({...proyectoForm, objetivo: e.target.value})} /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Vigencia Inicio</label><input type="number" className="input" value={proyectoForm.vigencia_inicio} onChange={e => setProyectoForm({...proyectoForm, vigencia_inicio: +e.target.value})} /></div>
            <div><label className="label">Vigencia Fin</label><input type="number" className="input" value={proyectoForm.vigencia_fin} onChange={e => setProyectoForm({...proyectoForm, vigencia_fin: +e.target.value})} /></div>
          </div>
          <div><label className="label">Estado</label><select className="input" value={proyectoForm.estado} onChange={e => setProyectoForm({...proyectoForm, estado: e.target.value})}><option value="FORMULACION">Formulación</option><option value="EJECUCION">Ejecución</option><option value="TERMINADO">Terminado</option><option value="SUSPENDIDO">Suspendido</option><option value="CANCELADO">Cancelado</option></select></div>
          <div><label className="label">Fuente Origen</label><input className="input" value={proyectoForm.fuente_origen} onChange={e => setProyectoForm({...proyectoForm, fuente_origen: e.target.value})} /></div>
          <div className="flex justify-end gap-2 pt-2"><button onClick={() => { setShowProyectoForm(false); setEditProyecto(null); }} className="btn-secondary">Cancelar</button><button onClick={saveProyecto} className="btn-primary">Guardar</button></div>
        </div>
      </Modal>

      <Modal isOpen={showContratoForm} onClose={() => { setShowContratoForm(false); setEditContrato(null); setSelectedProyectoId(""); }} title={editContrato ? "Editar Contrato" : "Nuevo Contrato"}>
        <div className="space-y-4">
          <div><label className="label">Número</label><input className="input" value={contratoForm.numero} onChange={e => setContratoForm({...contratoForm, numero: e.target.value})} /></div>
          <div><label className="label">SECOP ID</label><input className="input" value={contratoForm.secop_id} onChange={e => setContratoForm({...contratoForm, secop_id: e.target.value})} /></div>
          <div><label className="label">Objeto</label><textarea className="input" rows={2} value={contratoForm.objeto} onChange={e => setContratoForm({...contratoForm, objeto: e.target.value})} /></div>
          <div><label className="label">Contratista</label><input className="input" value={contratoForm.contratista} onChange={e => setContratoForm({...contratoForm, contratista: e.target.value})} /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Valor Inicial</label><input type="number" className="input" value={contratoForm.valor_inicial} onChange={e => setContratoForm({...contratoForm, valor_inicial: +e.target.value})} /></div>
            <div><label className="label">Valor Actual</label><input type="number" className="input" value={contratoForm.valor_actual} onChange={e => setContratoForm({...contratoForm, valor_actual: +e.target.value})} /></div>
          </div>
          <div><label className="label">Estado</label><select className="input" value={contratoForm.estado} onChange={e => setContratoForm({...contratoForm, estado: e.target.value})}><option value="EN_EJECUCION">En Ejecución</option><option value="SUSPENDIDO">Suspendido</option><option value="TERMINADO">Terminado</option><option value="LIQUIDADO">Liquidado</option><option value="CANCELADO">Cancelado</option></select></div>
          <div className="flex justify-end gap-2 pt-2"><button onClick={() => { setShowContratoForm(false); setEditContrato(null); setSelectedProyectoId(""); }} className="btn-secondary">Cancelar</button><button onClick={saveContrato} className="btn-primary">Guardar</button></div>
        </div>
      </Modal>

      <Modal isOpen={showPresupuestoForm} onClose={() => { setShowPresupuestoForm(false); setEditPresupuesto(null); setSelectedProyectoPresupuesto(""); }} title={editPresupuesto ? "Editar Presupuesto" : "Nuevo Presupuesto"}>
        <div className="space-y-4">
          <div><label className="label">Vigencia</label><input type="number" className="input" value={presupuestoForm.vigencia} onChange={e => setPresupuestoForm({...presupuestoForm, vigencia: +e.target.value})} /></div>
          <div><label className="label">Fuente</label><input className="input" value={presupuestoForm.fuente} onChange={e => setPresupuestoForm({...presupuestoForm, fuente: e.target.value})} /></div>
          <div><label className="label">Apropiación Inicial</label><input type="number" className="input" value={presupuestoForm.apropiacion_inicial} onChange={e => setPresupuestoForm({...presupuestoForm, apropiacion_inicial: +e.target.value})} /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Adiciones</label><input type="number" className="input" value={presupuestoForm.adiciones} onChange={e => setPresupuestoForm({...presupuestoForm, adiciones: +e.target.value})} /></div>
            <div><label className="label">Reducciones</label><input type="number" className="input" value={presupuestoForm.reducciones} onChange={e => setPresupuestoForm({...presupuestoForm, reducciones: +e.target.value})} /></div>
          </div>
          <div><label className="label">Apropiación Definitiva</label><input type="number" className="input" value={presupuestoForm.apropiacion_definitiva} onChange={e => setPresupuestoForm({...presupuestoForm, apropiacion_definitiva: +e.target.value})} /></div>
          <div className="flex justify-end gap-2 pt-2"><button onClick={() => { setShowPresupuestoForm(false); setEditPresupuesto(null); setSelectedProyectoPresupuesto(""); }} className="btn-secondary">Cancelar</button><button onClick={savePresupuesto} className="btn-primary">Guardar</button></div>
        </div>
      </Modal>
    </div>
  );
}
