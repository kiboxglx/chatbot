import { useState, useEffect } from 'react';
import axios from 'axios';
import {
    Users,
    UserPlus,
    Search,
    Trash2,
    Settings as SettingsIcon,
    Save,
    LayoutDashboard,
    Activity,
    MessageSquare,
    CheckCircle2,
    AlertCircle,
    X
} from 'lucide-react';

// Configuração da API
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface Client {
    id: number;
    nome: string;
    telefone: string;
    empresa_nome: string;
    cnpj_cpf: string;
}

interface SettingsData {
    system_prompt: string;
    active: boolean;
}

interface ConnectionStatus {
    state: string;
    instance?: {
        state: string;
    };
}

// Componente de Toast Simples
const Toast = ({ message, type, onClose }: { message: string, type: 'success' | 'error', onClose: () => void }) => (
    <div className={`fixed top-4 right-4 z-50 flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg transform transition-all duration-300 ${type === 'success' ? 'bg-emerald-600 text-white' : 'bg-red-600 text-white'
        }`}>
        {type === 'success' ? <CheckCircle2 size={20} /> : <AlertCircle size={20} />}
        <span className="font-medium">{message}</span>
        <button onClick={onClose} className="ml-2 hover:bg-white/20 rounded-full p-1">
            <X size={16} />
        </button>
    </div>
);

function App() {
    const [activeTab, setActiveTab] = useState<'dashboard' | 'clients' | 'settings' | 'connection'>('dashboard');
    const [clients, setClients] = useState<Client[]>([]);
    const [settings, setSettings] = useState<SettingsData>({ system_prompt: '', active: true });
    const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({ state: 'CHECKING' });
    const [qrCode, setQrCode] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [formData, setFormData] = useState({ nome: '', telefone: '', empresa_nome: '', cnpj_cpf: '' });
    const [toast, setToast] = useState<{ message: string, type: 'success' | 'error' } | null>(null);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchClients();
        fetchSettings();
        checkConnection();
    }, []);

    // Polling para verificar status da conexão a cada 10s se estiver na aba de conexão
    useEffect(() => {
        let interval: any;
        if (activeTab === 'connection') {
            checkConnection();
            interval = setInterval(checkConnection, 5000);
        }
        return () => clearInterval(interval);
    }, [activeTab]);

    const showToast = (message: string, type: 'success' | 'error') => {
        setToast({ message, type });
        setTimeout(() => setToast(null), 3000);
    };

    const checkConnection = async () => {
        try {
            const response = await axios.get(`${API_URL}/management/status`);
            setConnectionStatus(response.data);

            if (response.data.instance?.state === 'open' || response.data.state === 'open') {
                setQrCode(null);
            } else if (activeTab === 'connection' && !qrCode) {
                // Se desconectado e na aba, tenta pegar QR Code
                fetchQrCode();
            }
        } catch (error) {
            console.error("Erro ao checar conexão", error);
        }
    };

    const fetchQrCode = async () => {
        try {
            const response = await axios.get(`${API_URL}/management/qrcode`);
            if (response.data.base64) {
                setQrCode(response.data.base64);
            } else if (response.data.code) {
                setQrCode(response.data.code); // Algumas versões retornam 'code'
            }
        } catch (error) {
            console.error("Erro ao pegar QR Code", error);
        }
    };

    const handleLogout = async () => {
        if (confirm("Tem certeza que deseja desconectar o WhatsApp?")) {
            try {
                await axios.post(`${API_URL}/management/logout`);
                showToast("Desconectado com sucesso.", "success");
                checkConnection();
                fetchQrCode();
            } catch (error) {
                showToast("Erro ao desconectar.", "error");
            }
        }
    };

    const fetchClients = async () => {
        try {
            const response = await axios.get(`${API_URL}/clients`);
            setClients(response.data);
        } catch (error) {
            console.error("Erro ao buscar clientes", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchSettings = async () => {
        try {
            const response = await axios.get(`${API_URL}/settings`);
            setSettings(response.data);
        } catch (error) {
            console.error("Erro ao buscar configurações", error);
        }
    };

    const handleSaveSettings = async () => {
        try {
            await axios.post(`${API_URL}/settings`, settings);
            showToast("Configurações salvas com sucesso!", "success");
        } catch (error) {
            showToast("Erro ao salvar configurações.", "error");
        }
    };

    const toggleBot = async () => {
        const newSettings = { ...settings, active: !settings.active };
        setSettings(newSettings);
        try {
            await axios.post(`${API_URL}/settings`, newSettings);
            showToast(`Bot ${newSettings.active ? 'ATIVADO' : 'DESATIVADO'} com sucesso!`, "success");
        } catch (error) {
            showToast("Erro ao alterar status do bot.", "error");
            setSettings(settings); // Reverte em caso de erro
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await axios.post(`${API_URL}/clients`, formData);
            setShowModal(false);
            setFormData({ nome: '', telefone: '', empresa_nome: '', cnpj_cpf: '' });
            fetchClients();
            showToast("Cliente cadastrado com sucesso!", "success");
        } catch (error: any) {
            const errorMessage = error.response?.data?.detail || "Erro ao salvar cliente.";
            showToast(errorMessage, "error");
        }
    };

    const handleDelete = async (id: number) => {
        if (confirm("Tem certeza que deseja excluir este cliente?")) {
            try {
                await axios.delete(`${API_URL}/clients/${id}`);
                fetchClients();
                showToast("Cliente removido.", "success");
            } catch (error) {
                showToast("Erro ao excluir cliente.", "error");
            }
        }
    };

    const filteredClients = clients.filter(client =>
        client.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
        client.empresa_nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
        client.telefone.includes(searchTerm) ||
        client.cnpj_cpf.includes(searchTerm)
    );

    return (
        <div className="min-h-screen bg-gray-900 text-gray-100 flex font-sans">

            {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

            {/* Sidebar */}
            <aside className="w-72 bg-gray-800 border-r border-gray-700 p-6 flex flex-col shadow-xl z-10">
                <div className="flex items-center gap-3 mb-10 px-2">
                    <div className="w-10 h-10 bg-emerald-500 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-500/20">
                        <MessageSquare className="text-white" size={24} />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold text-white">Ana Chatbot</h1>
                        <p className="text-xs text-emerald-400 font-medium">Secretária Virtual</p>
                    </div>
                </div>

                <nav className="space-y-2 flex-1">
                    <button
                        onClick={() => setActiveTab('dashboard')}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 font-medium ${activeTab === 'dashboard' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/20' : 'text-gray-400 hover:bg-gray-700/50 hover:text-white'}`}
                    >
                        <LayoutDashboard size={20} />
                        Visão Geral
                    </button>
                    <button
                        onClick={() => setActiveTab('connection')}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 font-medium ${activeTab === 'connection' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/20' : 'text-gray-400 hover:bg-gray-700/50 hover:text-white'}`}
                    >
                        <Activity size={20} />
                        Conexão WhatsApp
                    </button>
                    <button
                        onClick={() => setActiveTab('clients')}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 font-medium ${activeTab === 'clients' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/20' : 'text-gray-400 hover:bg-gray-700/50 hover:text-white'}`}
                    >
                        <Users size={20} />
                        Meus Clientes
                    </button>
                    <button
                        onClick={() => setActiveTab('settings')}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 font-medium ${activeTab === 'settings' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/20' : 'text-gray-400 hover:bg-gray-700/50 hover:text-white'}`}
                    >
                        <SettingsIcon size={20} />
                        Inteligência da Ana
                    </button>
                </nav>

                <div className="mt-auto pt-6 border-t border-gray-700">
                    <div className="flex items-center gap-3 px-2">
                        <div className={`w-3 h-3 rounded-full ${settings.active ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></div>
                        <span className="text-sm text-gray-400">Sistema {settings.active ? 'Online' : 'Offline'}</span>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 p-8 overflow-y-auto bg-gray-900">

                {activeTab === 'dashboard' && (
                    <div className="max-w-5xl mx-auto animate-fade-in">
                        <header className="mb-10">
                            <h2 className="text-3xl font-bold text-white mb-2">Olá, Contador! 👋</h2>
                            <p className="text-gray-400">Aqui está o resumo da sua operação hoje.</p>
                        </header>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                            {/* Status Card */}
                            <div className={`p-6 rounded-2xl border transition-all duration-300 ${settings.active ? 'bg-emerald-500/10 border-emerald-500/20' : 'bg-red-500/10 border-red-500/20'}`}>
                                <div className="flex justify-between items-start mb-4">
                                    <div className={`p-3 rounded-xl ${settings.active ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white'}`}>
                                        <Activity size={24} />
                                    </div>
                                    <label className="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" className="sr-only peer" checked={settings.active} onChange={toggleBot} />
                                        <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-emerald-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                                    </label>
                                </div>
                                <h3 className="text-lg font-semibold text-white mb-1">Status do Robô</h3>
                                <p className={`text-sm ${settings.active ? 'text-emerald-400' : 'text-red-400'}`}>
                                    {settings.active ? 'Atendendo clientes automaticamente' : 'Pausado (Não responde ninguém)'}
                                </p>
                            </div>

                            {/* Connection Card */}
                            <div onClick={() => setActiveTab('connection')} className="bg-gray-800 p-6 rounded-2xl border border-gray-700 hover:border-gray-600 transition-colors cursor-pointer">
                                <div className="flex items-center gap-4 mb-4">
                                    <div className={`p-3 rounded-xl ${connectionStatus.instance?.state === 'open' || connectionStatus.state === 'open' ? 'bg-blue-500/20 text-blue-400' : 'bg-orange-500/20 text-orange-400'}`}>
                                        <CheckCircle2 size={24} />
                                    </div>
                                </div>
                                <h3 className="text-lg font-bold text-white mb-1">
                                    {connectionStatus.instance?.state === 'open' || connectionStatus.state === 'open' ? 'WhatsApp Conectado' : 'WhatsApp Desconectado'}
                                </h3>
                                <p className="text-sm text-gray-400">Clique para gerenciar</p>
                            </div>

                            {/* Quick Action */}
                            <button
                                onClick={() => { setActiveTab('clients'); setShowModal(true); }}
                                className="bg-gray-800 p-6 rounded-2xl border border-gray-700 hover:border-emerald-500/50 hover:bg-gray-750 transition-all group text-left"
                            >
                                <div className="flex items-center gap-4 mb-4">
                                    <div className="p-3 bg-purple-500/20 text-purple-400 rounded-xl group-hover:bg-purple-500 group-hover:text-white transition-colors">
                                        <UserPlus size={24} />
                                    </div>
                                </div>
                                <h3 className="text-lg font-semibold text-white mb-1">Novo Cliente</h3>
                                <p className="text-sm text-gray-400">Cadastrar empresa rapidamente</p>
                            </button>
                        </div>
                    </div>
                )}

                {activeTab === 'connection' && (
                    <div className="max-w-4xl mx-auto animate-fade-in">
                        <header className="mb-8">
                            <h2 className="text-3xl font-bold text-white">Conexão WhatsApp</h2>
                            <p className="text-gray-400">Escaneie o QR Code para conectar o número do escritório.</p>
                        </header>

                        <div className="bg-gray-800 rounded-2xl border border-gray-700 p-8 shadow-xl flex flex-col items-center text-center">
                            {connectionStatus.instance?.state === 'open' || connectionStatus.state === 'open' ? (
                                <div className="py-10">
                                    <div className="w-24 h-24 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                                        <CheckCircle2 size={48} className="text-emerald-500" />
                                    </div>
                                    <h3 className="text-2xl font-bold text-white mb-2">WhatsApp Conectado!</h3>
                                    <p className="text-gray-400 mb-8">O sistema está pronto para enviar e receber mensagens.</p>

                                    <button
                                        onClick={handleLogout}
                                        className="bg-red-600/10 hover:bg-red-600 text-red-500 hover:text-white px-6 py-3 rounded-xl transition-all font-medium border border-red-600/20"
                                    >
                                        Desconectar WhatsApp
                                    </button>
                                </div>
                            ) : (
                                <div className="py-6">
                                    <div className="bg-white p-4 rounded-xl mb-6 inline-block">
                                        {qrCode ? (
                                            <img src={qrCode} alt="QR Code WhatsApp" className="w-64 h-64 object-contain" />
                                        ) : (
                                            <div className="w-64 h-64 flex items-center justify-center text-gray-400 bg-gray-100 rounded-lg">
                                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                                            </div>
                                        )}
                                    </div>
                                    <h3 className="text-xl font-bold text-white mb-2">Escaneie com seu celular</h3>
                                    <p className="text-gray-400 max-w-md mx-auto">
                                        Abra o WhatsApp no seu celular, vá em Configurações {'>'} Aparelhos Conectados {'>'} Conectar Aparelho.
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {activeTab === 'clients' && (
                    <div className="max-w-5xl mx-auto animate-fade-in">
                        <header className="flex justify-between items-center mb-8">
                            <div>
                                <h2 className="text-3xl font-bold text-white">Meus Clientes</h2>
                                <p className="text-gray-400">Gerencie quem tem acesso ao atendimento.</p>
                            </div>
                            <button
                                onClick={() => setShowModal(true)}
                                className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-xl transition-all shadow-lg shadow-emerald-900/20 font-medium"
                            >
                                <UserPlus size={20} />
                                Novo Cliente
                            </button>
                        </header>

                        <div className="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden shadow-xl">
                            <div className="p-6 border-b border-gray-700 flex justify-between items-center bg-gray-800/50">
                                <div className="relative w-full max-w-md">
                                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
                                    <input
                                        type="text"
                                        placeholder="Buscar por nome, empresa ou telefone..."
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl pl-12 pr-4 py-3 text-gray-200 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all"
                                    />
                                </div>
                            </div>

                            <div className="overflow-x-auto">
                                <table className="w-full text-left">
                                    <thead className="bg-gray-900/50 text-gray-400 uppercase text-xs font-medium">
                                        <tr>
                                            <th className="px-8 py-5">Nome</th>
                                            <th className="px-8 py-5">Empresa</th>
                                            <th className="px-8 py-5">Telefone</th>
                                            <th className="px-8 py-5">CNPJ/CPF</th>
                                            <th className="px-8 py-5 text-right">Ações</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-700">
                                        {loading ? (
                                            <tr><td colSpan={5} className="px-8 py-10 text-center text-gray-500">Carregando clientes...</td></tr>
                                        ) : filteredClients.length === 0 ? (
                                            <tr><td colSpan={5} className="px-8 py-10 text-center text-gray-500">Nenhum cliente encontrado.</td></tr>
                                        ) : filteredClients.map((client) => (
                                            <tr key={client.id} className="hover:bg-gray-700/30 transition-colors group">
                                                <td className="px-8 py-5 font-medium text-white">{client.nome}</td>
                                                <td className="px-8 py-5 text-gray-300">{client.empresa_nome}</td>
                                                <td className="px-8 py-5 text-gray-400 font-mono text-sm">{client.telefone}</td>
                                                <td className="px-8 py-5 text-gray-400 font-mono text-sm">{client.cnpj_cpf}</td>
                                                <td className="px-8 py-5 text-right">
                                                    <button
                                                        onClick={() => handleDelete(client.id)}
                                                        className="text-gray-500 hover:text-red-400 p-2 rounded-lg hover:bg-red-500/10 transition-colors"
                                                        title="Excluir Cliente"
                                                    >
                                                        <Trash2 size={18} />
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'settings' && (
                    <div className="max-w-4xl mx-auto animate-fade-in">
                        <header className="mb-8">
                            <h2 className="text-3xl font-bold text-white">Inteligência da Ana</h2>
                            <p className="text-gray-400">Configure como sua secretária virtual deve se comportar.</p>
                        </header>

                        <div className="bg-gray-800 rounded-2xl border border-gray-700 p-8 shadow-xl">
                            <div className="flex items-start gap-6 mb-8">
                                <div className="p-4 bg-emerald-500/10 rounded-xl">
                                    <MessageSquare size={32} className="text-emerald-500" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="text-xl font-bold text-white mb-2">Personalidade e Regras</h3>
                                    <p className="text-gray-400 text-sm leading-relaxed">
                                        Este é o "cérebro" da Ana. Tudo o que você escrever aqui servirá de instrução para ela.
                                        <br />
                                        <strong>Dica:</strong> Seja claro sobre o tom de voz (formal/informal) e o que ela NÃO deve fazer.
                                    </p>
                                </div>
                            </div>

                            <div className="mb-8">
                                <label className="block text-sm font-medium text-gray-300 mb-3 uppercase tracking-wider">Instruções do Sistema</label>
                                <div className="relative">
                                    <textarea
                                        value={settings.system_prompt}
                                        onChange={(e) => setSettings({ ...settings, system_prompt: e.target.value })}
                                        className="w-full h-96 bg-gray-900 border border-gray-700 rounded-xl p-6 text-gray-300 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none font-mono text-sm leading-relaxed resize-none shadow-inner"
                                        placeholder="Ex: Você é uma assistente contábil..."
                                    />
                                    <div className="absolute bottom-4 right-4 text-xs text-gray-600">
                                        Suporta Markdown
                                    </div>
                                </div>
                            </div>

                            <div className="flex items-center justify-between pt-6 border-t border-gray-700">
                                <div className="text-sm text-gray-500">
                                    Última alteração não salva...
                                </div>
                                <button
                                    onClick={handleSaveSettings}
                                    className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-3 rounded-xl transition-all shadow-lg shadow-emerald-900/20 font-bold"
                                >
                                    <Save size={20} />
                                    Salvar Alterações
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {/* Modal */}
                {showModal && (
                    <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 backdrop-blur-sm z-50 animate-fade-in">
                        <div className="bg-gray-800 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl transform transition-all scale-100">
                            <div className="flex justify-between items-center mb-6">
                                <h3 className="text-2xl font-bold text-white">Novo Cliente</h3>
                                <button onClick={() => setShowModal(false)} className="text-gray-400 hover:text-white">
                                    <X size={24} />
                                </button>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-5">
                                <div>
                                    <label className="block text-sm font-medium text-gray-400 mb-1.5">Nome Completo</label>
                                    <input
                                        required
                                        value={formData.nome}
                                        onChange={e => setFormData({ ...formData, nome: e.target.value })}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all"
                                        placeholder="Ex: João Silva"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-400 mb-1.5">Nome da Empresa</label>
                                    <input
                                        required
                                        value={formData.empresa_nome}
                                        onChange={e => setFormData({ ...formData, empresa_nome: e.target.value })}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all"
                                        placeholder="Ex: Silva LTDA"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-400 mb-1.5">WhatsApp (com DDD)</label>
                                    <input
                                        required
                                        placeholder="Ex: 5511999999999"
                                        value={formData.telefone}
                                        onChange={e => setFormData({ ...formData, telefone: e.target.value })}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all"
                                    />
                                    <p className="text-xs text-gray-500 mt-1">Importante: Use o formato internacional (55 + DDD + Número)</p>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-400 mb-1.5">CNPJ ou CPF</label>
                                    <input
                                        required
                                        value={formData.cnpj_cpf}
                                        onChange={e => setFormData({ ...formData, cnpj_cpf: e.target.value })}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all"
                                        placeholder="00.000.000/0001-00"
                                    />
                                </div>
                                <div className="flex justify-end gap-3 mt-8">
                                    <button
                                        type="button"
                                        onClick={() => setShowModal(false)}
                                        className="px-6 py-3 text-gray-400 hover:text-white font-medium transition-colors"
                                    >
                                        Cancelar
                                    </button>
                                    <button
                                        type="submit"
                                        className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-xl font-bold shadow-lg shadow-emerald-900/20 transition-all"
                                    >
                                        Salvar Cliente
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}

            </main>
        </div>
    );
}

export default App;
