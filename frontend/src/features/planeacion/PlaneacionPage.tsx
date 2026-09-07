"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { PlanDesarrollo, NodoPlan, Indicador, Meta, ProgramacionAnual, AvanceMeta } from "@/types";
import { formatNumber, getEstadoBadgeClass } from "@/lib/utils";
import Modal from "@/components/Modal";
import { Plus, ChevronDown, ChevronRight, Edit, Trash2, Target, Calendar, TrendingUp } from "lucide-react";

export default function PlaneacionPage() {
  const { token } = useAuth();
  const [tab, setTab] = useState<"planes" | "indicadores" | "metas">("planes");
  const [loading, setLoading] = useState(true);

  // Planes
  const [planes, setPlanes] = useState<PlanDesarrollo[]>([]);
  const [showPlanForm, setShowPlanForm] = useState(false);
  const [editPlan, setEditPlan] = useState<PlanDesarrollo | null>(null);
  const [selectedPlan, setSelectedPlan] = useState<PlanDesarrollo | null>(null);

  // Nodos
  const [nodos, setNodos] = useState<NodoPlan[]>([]);
  const [expandedNodos, setExpandedNodos] = useState<Set<string>>(new Set());
  const [showNodoForm, setShowNodoForm] = useState(false);
  const [editNodo, setEditNodo] = useState<NodoPlan | null>(null);
  const [nodoParent, setNodoParent] = useState<string | null>(null);

  // Indicadores
  const [indicadores, setIndicadores] = useState<Indicador[]>([]);
  const [showIndicadorForm, setShowIndicadorForm] = useState(false);
  const [editIndicador, setEditIndicador] = useState<Indicador | null>(null);

  // Metas
  const [metas, setMetas] = useState<Meta[]>([]);
  const [showMetaForm, setShowMetaForm] = useState(false);
  const [editMeta, setEditMeta] = useState<Meta | null>(null);
  const [selectedMeta, setSelectedMeta] = useState<Meta | null>(null);
  const [showAvanceForm, setShowAvanceForm] = useState(false);

  // Form states
  const [planForm, setPlanForm] = useState({ nombre: "", acuerdo_numero: "", vigencia_inicio: 2024, vigencia_fin: 2027 });
  const [nodoForm, setNodoForm] = useState({ tipo: "LINEA", codigo: "", nombre: "", orden: 0 });
  const [indicadorForm, setIndicadorForm] = useState({ codigo: "", nombre: "", descripcion: "", tipo: "CUANTITATIVO", unidad_medida: "", sentido: "POSITIVO", formula: "", fuente: "", periodicidad: "ANUAL" });
  const [metaForm, setMetaForm] = useState({ nodo_plan_id: "", indicador_id: "", dependencia_id: "", codigo: "", descripcion: "", linea_base: 0, meta_cuatrienio: 0, unidad_medida: "", ponderacion: 0 });
  const [avanceForm, setAvanceForm] = useState({ vigencia: 2024, periodo_tipo: "TRIMESTRE", periodo_numero: 1, fecha_corte: new Date().toISOString().split("T")[0], valor_periodo: 0 });
  const [progForm, setProgForm] = useState({ vigencia: 2024, valor_programado: 0 });
  const [showProgForm, setShowProgForm] = useState(false);

  const headers = { "Content-Type": "application/json" };

  const loadPlanes = useCallback(async () => {
    if (!token) return;
    const data = await api.get<PlanDesarrollo[]>("/planeacion/planes", token);
    setPlanes(data);
  }, [token]);

  const loadNodos = useCallback(async (planId: string) => {
    if (!token) return;
    const data = await api.get<NodoPlan[]>(`/planeacion/planes/${planId}/nodos`, token);
    setNodos(data);
  }, [token]);

  const loadIndicadores = useCallback(async () => {
    if (!token) return;
    const data = await api.get<Indicador[]>("/planeacion/indicadores", token);
    setIndicadores(data);
  }, [token]);

  const loadMetas = useCallback(async (planId: string) => {
    if (!token) return;
    const data = await api.get<Meta[]>(`/planeacion/planes/${planId}/metas`, token);
    setMetas(data);
  }, [token]);

  useEffect(() => {
    Promise.all([loadPlanes(), loadIndicadores()])
      .finally(() => setLoading(false));
  }, [loadPlanes, loadIndicadores]);

  useEffect(() => {
    if (selectedPlan) {
      loadNodos(selectedPlan.id);
      loadMetas(selectedPlan.id);
    }
  }, [selectedPlan, loadNodos, loadMetas]);

  // ─── Plan CRUD ───
  const savePlan = async () => {
    if (!token) return;
    if (editPlan) {
      await api.patch(`/planeacion/planes/${editPlan.id}`, planForm, token);
    } else {
      await api.post("/planeacion/planes", planForm, token);
    }
    setShowPlanForm(false);
    setEditPlan(null);
    loadPlanes();
  };

  const deletePlan = async (id: string) => {
    if (!confirm("¿Eliminar este plan?")) return;
    await api.delete(`/planeacion/planes/${id}`, token!);
    loadPlanes();
  };

  // ─── Nodo CRUD ───
  const saveNodo = async () => {
    if (!token || !selectedPlan) return;
    const body = { ...nodoForm, plan_id: selectedPlan.id, parent_id: nodoParent };
    if (editNodo) {
      await api.patch(`/planeacion/nodos/${editNodo.id}`, body, token);
    } else {
      await api.post(`/planeacion/planes/${selectedPlan.id}/nodos`, body, token);
    }
    setShowNodoForm(false);
    setEditNodo(null);
    setNodoParent(null);
    loadNodos(selectedPlan.id);
  };

  const deleteNodo = async (id: string) => {
    if (!confirm("¿Eliminar este nodo?")) return;
    await api.delete(`/planeacion/nodos/${id}`, token!);
    if (selectedPlan) loadNodos(selectedPlan.id);
  };

  // ─── Indicador CRUD ───
  const saveIndicador = async () => {
    if (!token) return;
    if (editIndicador) {
      await api.patch(`/planeacion/indicadores/${editIndicador.id}`, indicadorForm, token);
    } else {
      await api.post("/planeacion/indicadores", indicadorForm, token);
    }
    setShowIndicadorForm(false);
    setEditIndicador(null);
    loadIndicadores();
  };

  const deleteIndicador = async (id: string) => {
    if (!confirm("¿Eliminar este indicador?")) return;
    await api.delete(`/planeacion/indicadores/${id}`, token!);
    loadIndicadores();
  };

  // ─── Meta CRUD ───
  const saveMeta = async () => {
    if (!token || !selectedPlan) return;
    if (editMeta) {
      await api.patch(`/planeacion/metas/${editMeta.id}`, metaForm, token);
    } else {
      await api.post(`/planeacion/planes/${selectedPlan.id}/metas`, metaForm, token);
    }
    setShowMetaForm(false);
    setEditMeta(null);
    loadMetas(selectedPlan.id);
  };

  const deleteMeta = async (id: string) => {
    if (!confirm("¿Eliminar esta meta?")) return;
    await api.delete(`/planeacion/metas/${id}`, token!);
    if (selectedPlan) loadMetas(selectedPlan.id);
  };

  // ─── Avance ───
  const saveAvance = async () => {
    if (!token || !selectedMeta) return;
    await api.post(`/planeacion/metas/${selectedMeta.id}/avances`, avanceForm, token);
    setShowAvanceForm(false);
  };

  // ─── Programación ───
  const saveProgramacion = async () => {
    if (!token || !selectedMeta) return;
    await api.post(`/planeacion/metas/${selectedMeta.id}/programacion`, progForm, token);
    setShowProgForm(false);
  };

  const toggleNodo = (id: string) => {
    setExpandedNodos(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const renderNodoTree = (parentId: string | null, depth: number = 0) => {
    return nodos
      .filter(n => n.parent_id === parentId)
      .sort((a, b) => a.orden - b.orden)
      .map(nodo => {
        const hasChildren = nodos.some(n => n.parent_id === nodo.id);
        const isExpanded = expandedNodos.has(nodo.id);
        return (
          <div key={nodo.id} style={{ marginLeft: depth * 24 }}>
            <div className="flex items-center gap-2 py-2 px-3 hover:bg-gray-50 rounded-lg group">
              {hasChildren ? (
                <button onClick={() => toggleNodo(nodo.id)} className="p-0.5">
                  {isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                </button>
              ) : <span className="w-5" />}
              <span className="font-mono text-xs text-primary-600 bg-primary-50 px-1.5 py-0.5 rounded">{nodo.codigo}</span>
              <span className="text-sm text-gray-900 flex-1">{nodo.nombre}</span>
              <span className="text-xs text-gray-400">{nodo.tipo}</span>
              <div className="hidden group-hover:flex items-center gap-1">
                <button onClick={() => { setNodoParent(nodo.id); setNodoForm({ tipo: "LINEA", codigo: "", nombre: "", orden: 0 }); setShowNodoForm(true); }} className="p-1 hover:bg-gray-200 rounded"><Plus className="h-3.5 w-3.5" /></button>
                <button onClick={() => { setEditNodo(nodo); setNodoForm({ tipo: nodo.tipo, codigo: nodo.codigo, nombre: nodo.nombre, orden: nodo.orden }); setShowNodoForm(true); }} className="p-1 hover:bg-gray-200 rounded"><Edit className="h-3.5 w-3.5" /></button>
                <button onClick={() => deleteNodo(nodo.id)} className="p-1 hover:bg-red-100 rounded text-red-600"><Trash2 className="h-3.5 w-3.5" /></button>
              </div>
            </div>
            {isExpanded && hasChildren && renderNodoTree(nodo.id, depth + 1)}
          </div>
        );
      });
  };

  if (loading) {
    return <div className="space-y-4">{[...Array(3)].map((_, i) => <div key={i} className="h-24 bg-gray-100 rounded-xl animate-pulse" />)}</div>;
  }

  return (
    <div className="space-y-6">
      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-gray-200 pb-2">
        {([["planes", "Planes de Desarrollo"], ["indicadores", "Indicadores"], ["metas", "Metas y Avances"]] as const).map(([id, label]) => (
          <button key={id} onClick={() => setTab(id)} className={`px-4 py-2 text-sm font-medium rounded-t-lg ${tab === id ? "bg-primary-50 text-primary-700 border-b-2 border-primary-600" : "text-gray-500"}`}>
            {label}
          </button>
        ))}
      </div>

      {/* ─── PLANES TAB ─── */}
      {tab === "planes" && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <button onClick={() => { setEditPlan(null); setPlanForm({ nombre: "", acuerdo_numero: "", vigencia_inicio: 2024, vigencia_fin: 2027 }); setShowPlanForm(true); }} className="btn-primary flex items-center gap-2"><Plus className="h-4 w-4" /> Nuevo Plan</button>
          </div>
          {planes.length === 0 ? (
            <div className="card p-12 text-center text-gray-500">No hay planes registrados</div>
          ) : planes.map(plan => (
            <div key={plan.id} className={`card p-5 cursor-pointer transition-all ${selectedPlan?.id === plan.id ? "ring-2 ring-primary-500" : "hover:shadow-md"}`} onClick={() => setSelectedPlan(plan)}>
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-3">
                    <h3 className="font-semibold text-gray-900">{plan.nombre}</h3>
                    <span className={`badge ${getEstadoBadgeClass(plan.estado)}`}>{plan.estado}</span>
                  </div>
                  <p className="mt-1 text-sm text-gray-500">Vigencia: {plan.vigencia_inicio}-{plan.vigencia_fin} | v{plan.version}</p>
                  {plan.acuerdo_numero && <p className="text-xs text-gray-400 mt-1">Acuerdo: {plan.acuerdo_numero}</p>}
                </div>
                <div className="flex gap-2" onClick={e => e.stopPropagation()}>
                  <button onClick={() => { setEditPlan(plan); setPlanForm({ nombre: plan.nombre, acuerdo_numero: plan.acuerdo_numero || "", vigencia_inicio: plan.vigencia_inicio, vigencia_fin: plan.vigencia_fin }); setShowPlanForm(true); }} className="p-2 hover:bg-gray-100 rounded-lg"><Edit className="h-4 w-4 text-gray-500" /></button>
                  <button onClick={() => deletePlan(plan.id)} className="p-2 hover:bg-red-50 rounded-lg"><Trash2 className="h-4 w-4 text-red-500" /></button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ─── INDICADORES TAB ─── */}
      {tab === "indicadores" && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <button onClick={() => { setEditIndicador(null); setIndicadorForm({ codigo: "", nombre: "", descripcion: "", tipo: "CUANTITATIVO", unidad_medida: "", sentido: "POSITIVO", formula: "", fuente: "", periodicidad: "ANUAL" }); setShowIndicadorForm(true); }} className="btn-primary flex items-center gap-2"><Plus className="h-4 w-4" /> Nuevo Indicador</button>
          </div>
          <div className="card overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Código</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Unidad</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sentido</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Periodicidad</th>
                  <th className="px-4 py-3" />
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {indicadores.map(ind => (
                  <tr key={ind.id} className="hover:bg-gray-50 group">
                    <td className="px-4 py-3 text-sm font-mono text-gray-900">{ind.codigo}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{ind.nombre}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{ind.tipo}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{ind.unidad_medida}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{ind.sentido}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{ind.periodicidad}</td>
                    <td className="px-4 py-3 text-right hidden group-hover:table-cell">
                      <button onClick={() => { setEditIndicador(ind); setIndicadorForm({ codigo: ind.codigo, nombre: ind.nombre, descripcion: ind.descripcion || "", tipo: ind.tipo, unidad_medida: ind.unidad_medida, sentido: ind.sentido, formula: ind.formula || "", fuente: ind.fuente || "", periodicidad: ind.periodicidad }); setShowIndicadorForm(true); }} className="p-1 hover:bg-gray-200 rounded"><Edit className="h-3.5 w-3.5" /></button>
                      <button onClick={() => deleteIndicador(ind.id)} className="p-1 hover:bg-red-100 rounded text-red-600"><Trash2 className="h-3.5 w-3.5" /></button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ─── METAS TAB ─── */}
      {tab === "metas" && (
        <div className="space-y-4">
          {!selectedPlan ? (
            <div className="card p-12 text-center">
              <Target className="mx-auto h-12 w-12 text-gray-300" />
              <p className="mt-4 text-gray-500">Selecciona un Plan de Desarrollo en la pestaña &quot;Planes&quot; para ver sus metas</p>
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-500">Plan: <strong>{selectedPlan.nombre}</strong></p>
                <button onClick={() => { setEditMeta(null); setMetaForm({ nodo_plan_id: "", indicador_id: "", dependencia_id: "", codigo: "", descripcion: "", linea_base: 0, meta_cuatrienio: 0, unidad_medida: "", ponderacion: 0 }); setShowMetaForm(true); }} className="btn-primary flex items-center gap-2"><Plus className="h-4 w-4" /> Nueva Meta</button>
              </div>

              {/* Árbol de nodos */}
              <div className="card p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-medium text-gray-900">Estructura del Plan</h3>
                  <button onClick={() => { setNodoParent(null); setNodoForm({ tipo: "LINEA", codigo: "", nombre: "", orden: 0 }); setShowNodoForm(true); }} className="btn-secondary text-xs flex items-center gap-1"><Plus className="h-3 w-3" /> Nodo raíz</button>
                </div>
                <div className="space-y-0.5">
                  {nodos.filter(n => !n.parent_id).length === 0 ? (
                    <p className="text-sm text-gray-400 py-4 text-center">No hay nodos. Crea la estructura del plan.</p>
                  ) : renderNodoTree(null)}
                </div>
              </div>

              {/* Lista de metas */}
              {metas.length === 0 ? (
                <div className="card p-8 text-center text-gray-500">No hay metas registradas para este plan</div>
              ) : (
                <div className="space-y-3">
                  {metas.map(meta => {
                    const ind = indicadores.find(i => i.id === meta.indicador_id);
                    return (
                      <div key={meta.id} className="card p-4 hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <span className="font-mono text-xs bg-primary-50 text-primary-600 px-1.5 py-0.5 rounded">{meta.codigo}</span>
                              <span className={`badge ${getEstadoBadgeClass(meta.estado)}`}>{meta.estado}</span>
                            </div>
                            <p className="mt-1 text-sm text-gray-900">{meta.descripcion}</p>
                            <div className="mt-2 flex flex-wrap gap-3 text-xs text-gray-500">
                              {ind && <span>Indicador: {ind.nombre}</span>}
                              <span>Unidad: {meta.unidad_medida}</span>
                              <span>Meta cuatrienio: {formatNumber(meta.meta_cuatrienio)}</span>
                              {meta.linea_base != null && <span>Línea base: {formatNumber(meta.linea_base)}</span>}
                              {meta.ponderacion != null && <span>Ponderación: {meta.ponderacion}%</span>}
                            </div>
                          </div>
                          <div className="flex gap-1">
                            <button onClick={() => { setSelectedMeta(meta); setShowAvanceForm(true); }} className="p-2 hover:bg-blue-50 rounded-lg" title="Registrar avance"><TrendingUp className="h-4 w-4 text-blue-500" /></button>
                            <button onClick={() => { setSelectedMeta(meta); setShowProgForm(true); }} className="p-2 hover:bg-green-50 rounded-lg" title="Programación anual"><Calendar className="h-4 w-4 text-green-500" /></button>
                            <button onClick={() => { setEditMeta(meta); setMetaForm({ nodo_plan_id: meta.nodo_plan_id, indicador_id: meta.indicador_id, dependencia_id: meta.dependencia_id, codigo: meta.codigo, descripcion: meta.descripcion, linea_base: meta.linea_base || 0, meta_cuatrienio: meta.meta_cuatrienio, unidad_medida: meta.unidad_medida, ponderacion: meta.ponderacion || 0 }); setShowMetaForm(true); }} className="p-2 hover:bg-gray-100 rounded-lg"><Edit className="h-4 w-4 text-gray-500" /></button>
                            <button onClick={() => deleteMeta(meta.id)} className="p-2 hover:bg-red-50 rounded-lg"><Trash2 className="h-4 w-4 text-red-500" /></button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* ─── MODALS ─── */}
      <Modal isOpen={showPlanForm} onClose={() => { setShowPlanForm(false); setEditPlan(null); }} title={editPlan ? "Editar Plan" : "Nuevo Plan de Desarrollo"}>
        <div className="space-y-4">
          <div><label className="label">Nombre</label><input className="input" value={planForm.nombre} onChange={e => setPlanForm({...planForm, nombre: e.target.value})} /></div>
          <div><label className="label">Acuerdo Número</label><input className="input" value={planForm.acuerdo_numero} onChange={e => setPlanForm({...planForm, acuerdo_numero: e.target.value})} /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Vigencia Inicio</label><input type="number" className="input" value={planForm.vigencia_inicio} onChange={e => setPlanForm({...planForm, vigencia_inicio: +e.target.value})} /></div>
            <div><label className="label">Vigencia Fin</label><input type="number" className="input" value={planForm.vigencia_fin} onChange={e => setPlanForm({...planForm, vigencia_fin: +e.target.value})} /></div>
          </div>
          <div className="flex justify-end gap-2 pt-2"><button onClick={() => { setShowPlanForm(false); setEditPlan(null); }} className="btn-secondary">Cancelar</button><button onClick={savePlan} className="btn-primary">Guardar</button></div>
        </div>
      </Modal>

      <Modal isOpen={showNodoForm} onClose={() => { setShowNodoForm(false); setEditNodo(null); setNodoParent(null); }} title={editNodo ? "Editar Nodo" : "Nuevo Nodo"}>
        <div className="space-y-4">
          <div><label className="label">Tipo</label><select className="input" value={nodoForm.tipo} onChange={e => setNodoForm({...nodoForm, tipo: e.target.value})}><option value="LINEA">Línea</option><option value="SECTOR">Sector</option><option value="PROGRAMA">Programa</option><option value="PRODUCTO">Producto</option><option value="OTRO">Otro</option></select></div>
          <div><label className="label">Código</label><input className="input" value={nodoForm.codigo} onChange={e => setNodoForm({...nodoForm, codigo: e.target.value})} /></div>
          <div><label className="label">Nombre</label><input className="input" value={nodoForm.nombre} onChange={e => setNodoForm({...nodoForm, nombre: e.target.value})} /></div>
          <div><label className="label">Orden</label><input type="number" className="input" value={nodoForm.orden} onChange={e => setNodoForm({...nodoForm, orden: +e.target.value})} /></div>
          {nodoParent && <p className="text-xs text-gray-400">Padre: {nodos.find(n => n.id === nodoParent)?.nombre}</p>}
          <div className="flex justify-end gap-2 pt-2"><button onClick={() => { setShowNodoForm(false); setEditNodo(null); setNodoParent(null); }} className="btn-secondary">Cancelar</button><button onClick={saveNodo} className="btn-primary">Guardar</button></div>
        </div>
      </Modal>

      <Modal isOpen={showIndicadorForm} onClose={() => { setShowIndicadorForm(false); setEditIndicador(null); }} title={editIndicador ? "Editar Indicador" : "Nuevo Indicador"}>
        <div className="space-y-4">
          <div><label className="label">Código</label><input className="input" value={indicadorForm.codigo} onChange={e => setIndicadorForm({...indicadorForm, codigo: e.target.value})} /></div>
          <div><label className="label">Nombre</label><input className="input" value={indicadorForm.nombre} onChange={e => setIndicadorForm({...indicadorForm, nombre: e.target.value})} /></div>
          <div><label className="label">Descripción</label><textarea className="input" rows={2} value={indicadorForm.descripcion} onChange={e => setIndicadorForm({...indicadorForm, descripcion: e.target.value})} /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Tipo</label><select className="input" value={indicadorForm.tipo} onChange={e => setIndicadorForm({...indicadorForm, tipo: e.target.value})}><option value="CUANTITATIVO">Cuantitativo</option><option value="CUALITATIVO">Cualitativo</option></select></div>
            <div><label className="label">Sentido</label><select className="input" value={indicadorForm.sentido} onChange={e => setIndicadorForm({...indicadorForm, sentido: e.target.value})}><option value="POSITIVO">Positivo</option><option value="NEGATIVO">Negativo</option><option value="NEUTRO">Neutro</option></select></div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Unidad de Medida</label><input className="input" value={indicadorForm.unidad_medida} onChange={e => setIndicadorForm({...indicadorForm, unidad_medida: e.target.value})} /></div>
            <div><label className="label">Periodicidad</label><select className="input" value={indicadorForm.periodicidad} onChange={e => setIndicadorForm({...indicadorForm, periodicidad: e.target.value})}><option value="ANUAL">Anual</option><option value="SEMESTRAL">Semestral</option><option value="TRIMESTRAL">Trimestral</option><option value="MENSUAL">Mensual</option></select></div>
          </div>
          <div><label className="label">Fórmula</label><input className="input" value={indicadorForm.formula} onChange={e => setIndicadorForm({...indicadorForm, formula: e.target.value})} /></div>
          <div><label className="label">Fuente</label><input className="input" value={indicadorForm.fuente} onChange={e => setIndicadorForm({...indicadorForm, fuente: e.target.value})} /></div>
          <div className="flex justify-end gap-2 pt-2"><button onClick={() => { setShowIndicadorForm(false); setEditIndicador(null); }} className="btn-secondary">Cancelar</button><button onClick={saveIndicador} className="btn-primary">Guardar</button></div>
        </div>
      </Modal>

      <Modal isOpen={showMetaForm} onClose={() => { setShowMetaForm(false); setEditMeta(null); }} title={editMeta ? "Editar Meta" : "Nueva Meta"}>
        <div className="space-y-4">
          <div><label className="label">Código</label><input className="input" value={metaForm.codigo} onChange={e => setMetaForm({...metaForm, codigo: e.target.value})} /></div>
          <div><label className="label">Descripción</label><textarea className="input" rows={2} value={metaForm.descripcion} onChange={e => setMetaForm({...metaForm, descripcion: e.target.value})} /></div>
          <div><label className="label">Nodo del Plan</label><select className="input" value={metaForm.nodo_plan_id} onChange={e => setMetaForm({...metaForm, nodo_plan_id: e.target.value})}><option value="">Seleccionar...</option>{nodos.map(n => <option key={n.id} value={n.id}>{n.codigo} - {n.nombre}</option>)}</select></div>
          <div><label className="label">Indicador</label><select className="input" value={metaForm.indicador_id} onChange={e => setMetaForm({...metaForm, indicador_id: e.target.value})}><option value="">Seleccionar...</option>{indicadores.map(i => <option key={i.id} value={i.id}>{i.codigo} - {i.nombre}</option>)}</select></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Unidad de Medida</label><input className="input" value={metaForm.unidad_medida} onChange={e => setMetaForm({...metaForm, unidad_medida: e.target.value})} /></div>
            <div><label className="label">Ponderación (%)</label><input type="number" className="input" value={metaForm.ponderacion} onChange={e => setMetaForm({...metaForm, ponderacion: +e.target.value})} /></div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Línea Base</label><input type="number" className="input" value={metaForm.linea_base} onChange={e => setMetaForm({...metaForm, linea_base: +e.target.value})} /></div>
            <div><label className="label">Meta Cuatrienio</label><input type="number" className="input" value={metaForm.meta_cuatrienio} onChange={e => setMetaForm({...metaForm, meta_cuatrienio: +e.target.value})} /></div>
          </div>
          <div className="flex justify-end gap-2 pt-2"><button onClick={() => { setShowMetaForm(false); setEditMeta(null); }} className="btn-secondary">Cancelar</button><button onClick={saveMeta} className="btn-primary">Guardar</button></div>
        </div>
      </Modal>

      <Modal isOpen={showAvanceForm} onClose={() => { setShowAvanceForm(false); setSelectedMeta(null); }} title={`Registrar Avance — ${selectedMeta?.codigo || ""}`}>
        <div className="space-y-4">
          <div><label className="label">Vigencia</label><input type="number" className="input" value={avanceForm.vigencia} onChange={e => setAvanceForm({...avanceForm, vigencia: +e.target.value})} /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="label">Periodo Tipo</label><select className="input" value={avanceForm.periodo_tipo} onChange={e => setAvanceForm({...avanceForm, periodo_tipo: e.target.value})}><option value="TRIMESTRE">Trimestre</option><option value="SEMESTRE">Semestre</option><option value="MES">Mes</option></select></div>
            <div><label className="label">Periodo Número</label><input type="number" className="input" value={avanceForm.periodo_numero} onChange={e => setAvanceForm({...avanceForm, periodo_numero: +e.target.value})} /></div>
          </div>
          <div><label className="label">Fecha de Corte</label><input type="date" className="input" value={avanceForm.fecha_corte} onChange={e => setAvanceForm({...avanceForm, fecha_corte: e.target.value})} /></div>
          <div><label className="label">Valor del Periodo</label><input type="number" className="input" value={avanceForm.valor_periodo} onChange={e => setAvanceForm({...avanceForm, valor_periodo: +e.target.value})} /></div>
          <div className="flex justify-end gap-2 pt-2"><button onClick={() => { setShowAvanceForm(false); setSelectedMeta(null); }} className="btn-secondary">Cancelar</button><button onClick={saveAvance} className="btn-primary">Guardar</button></div>
        </div>
      </Modal>

      <Modal isOpen={showProgForm} onClose={() => { setShowProgForm(false); setSelectedMeta(null); }} title={`Programación Anual — ${selectedMeta?.codigo || ""}`}>
        <div className="space-y-4">
          <div><label className="label">Vigencia</label><input type="number" className="input" value={progForm.vigencia} onChange={e => setProgForm({...progForm, vigencia: +e.target.value})} /></div>
          <div><label className="label">Valor Programado</label><input type="number" className="input" value={progForm.valor_programado} onChange={e => setProgForm({...progForm, valor_programado: +e.target.value})} /></div>
          <div className="flex justify-end gap-2 pt-2"><button onClick={() => { setShowProgForm(false); setSelectedMeta(null); }} className="btn-secondary">Cancelar</button><button onClick={saveProgramacion} className="btn-primary">Guardar</button></div>
        </div>
      </Modal>
    </div>
  );
}
