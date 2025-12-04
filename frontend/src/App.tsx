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
    X,
    LogOut
} from 'lucide-react';
import { Sidebar, SidebarBody, SidebarLink } from "@/components/ui/sidebar";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

// Configuração da API
// Em produção, usa a URL do Railway se a variável de ambiente não estiver definida
const API_URL = import.meta.env.VITE_API_URL || 'https://chatbot-production.up.railway.app';

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
    <div className={`fixed top-4 right-4 z-[60] flex items-center gap-3 px-4 py-3 rounded-xl shadow-2xl transform transition-all duration-300 animate-fade-in ${type === 'success' ? 'bg-emerald-600/90 text-white backdrop-blur-md' : 'bg-red-600/90 text-white backdrop-blur-md'
        }`}>
        {type === 'success' ? <CheckCircle2 size={20} /> : <AlertCircle size={20} />}
        <span className="font-medium text-sm">{message}</span>
        <button onClick={onClose} className="ml-2 hover:bg-white/20 rounded-full p-1">
            <X size={16} />
        </button>
    </div>
);

const Logo = () => {
    return (
        <div className="font-normal flex space-x-2 items-center text-sm text-black py-1 relative z-20">
            <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center shadow-lg shadow-emerald-500/20 flex-shrink-0">
                <MessageSquare className="text-white" size={18} />
            </div>
            <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="font-bold text-lg text-white whitespace-pre"
            >
                Ana Chatbot
            </motion.span>
        </div>
    );
};

const LogoIcon = () => {
    return (
        <div className="font-normal flex space-x-2 items-center text-sm text-black py-1 relative z-20">
            <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center shadow-lg shadow-emerald-500/20 flex-shrink-0">
                <MessageSquare className="text-white" size={18} />
            </div>
        </div>
    );
};

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
    const [open, setOpen] = useState(false);

    useEffect(() => {
        fetchClients();
        fetchSettings();
        checkConnection();
    }, []);

    // Polling para verificar status da conexão
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
                setQrCode(response.data.code);
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
            setSettings(settings);
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

    const links = [
        {
            label: "Visão Geral",
            href: "#",
            icon: <LayoutDashboard className="text-neutral-200 h-5 w-5 flex-shrink-0" />,
            onClick: () => setActiveTab('dashboard')
        },
        {
            label: "Conexão WhatsApp",
            href: "#",
            icon: <Activity className="text-neutral-200 h-5 w-5 flex-shrink-0" />,
            onClick: () => setActiveTab('connection')
        },
        {
            label: "Meus Clientes",
            href: "#",
            icon: <Users className="text-neutral-200 h-5 w-5 flex-shrink-0" />,
            onClick: () => setActiveTab('clients')
        },
        {
            label: "Inteligência da Ana",
            href: "#",
            icon: <SettingsIcon className="text-neutral-200 h-5 w-5 flex-shrink-0" />,
            onClick: () => setActiveTab('settings')
        }
    ];

    return (
        <div className={cn(
            "rounded-md flex flex-col lg:flex-row bg-gray-900 w-full flex-1 max-w-full mx-auto border border-neutral-700 overflow-hidden h-screen"
        )}>
            {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

            <Sidebar open={open} setOpen={setOpen}>
                <SidebarBody className="justify-between gap-10 bg-gray-800 border-r border-gray-700">
                    <div className="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
                        {open ? <Logo /> : <LogoIcon />}
                        <div className="mt-8 flex flex-col gap-2">
                            {links.map((link, idx) => (
                                <SidebarLink key={idx} link={link} className={activeTab === ['dashboard', 'connection', 'clients', 'settings'][idx] ? "bg-gray-700/50 rounded-lg" : ""} />
                            ))}
                        </div>
                    </div>
                    <div>
                        <div className="flex items-center gap-2 p-2">
                            <div className={`w-3 h-3 rounded-full ${settings.active ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></div>
                            {open && (
                                <motion.span
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="text-sm text-gray-400 whitespace-pre"
                                >
                                    Sistema {settings.active ? 'Online' : 'Offline'}
                                </motion.span>
                            )}
                        </div>
                    </div>
                </SidebarBody>
            </Sidebar>

            {/* Main Content */}
            <main className="flex-1 p-4 md:p-8 overflow-y-auto bg-gray-900">

                {activeTab === 'dashboard' && (
                    <div className="max-w-5xl mx-auto animate-fade-in space-y-6">
                        <header className="md:mb-10">
                            <h2 className="text-2xl md:text-3xl font-bold text-white mb-1">Olá, Contador! 👋</h2>
                            <p className="text-gray-400 text-sm md:text-base">Resumo da sua operação hoje.</p>
                        </header>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
                            {/* Status Card */}
                            <div className={`p-6 rounded-2xl border transition-all duration-300 relative overflow-hidden ${settings.active ? 'bg-gradient-to-br from-emerald-500/10 to-emerald-900/10 border-emerald-500/20' : 'bg-gradient-to-br from-red-500/10 to-red-900/10 border-red-500/20'}`}>
                                <div className="flex justify-between items-start mb-4 relative z-10">
                                    <div className={`p-3 rounded-xl ${settings.active ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20' : 'bg-red-500 text-white shadow-lg shadow-red-500/20'}`}>
                                        <Activity size={24} />
                                    </div>
                                    <label className="relative inline-flex items-center cursor-pointer active:scale-95 transition-transform">
                                        <input type="checkbox" className="sr-only peer" checked={settings.active} onChange={toggleBot} />
                                        <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
                                    </label>
                                </div>
                                <h3 className="text-lg font-semibold text-white mb-1 relative z-10">Status do Robô</h3>
                                <p className={`text-sm relative z-10 ${settings.active ? 'text-emerald-400' : 'text-red-400'}`}>
                                    {settings.active ? 'Ativo e respondendo' : 'Pausado'}
                                </p>
                            </div>

                            {/* Connection Card */}
                            <div onClick={() => setActiveTab('connection')} className="bg-gray-800 p-6 rounded-2xl border border-gray-700 active:scale-[0.98] hover:border-gray-600 transition-all cursor-pointer relative group">
                                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl"></div>
                                <div className="flex items-center gap-4 mb-4 relative z-10">
                                    <div className={`p-3 rounded-xl ${connectionStatus.instance?.state === 'open' || connectionStatus.state === 'open' ? 'bg-blue-500/20 text-blue-400' : 'bg-orange-500/20 text-orange-400'}`}>
                                        <CheckCircle2 size={24} />
                                    </div>
                                </div>
                                <h3 className="text-lg font-bold text-white mb-1 relative z-10">
                                    {connectionStatus.instance?.state === 'open' || connectionStatus.state === 'open' ? 'WhatsApp Conectado' : 'WhatsApp Desconectado'}
                                </h3>
                                <p className="text-sm text-gray-400 relative z-10">Toque para gerenciar</p>
                            </div>

                            {/* Quick Action */}
                            <button
                                onClick={() => { setActiveTab('clients'); setShowModal(true); }}
                                className="bg-gray-800 p-6 rounded-2xl border border-gray-700 active:scale-[0.98] hover:border-emerald-500/50 hover:bg-gray-750 transition-all group text-left relative overflow-hidden"
                            >
                                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                <div className="flex items-center gap-4 mb-4 relative z-10">
                                    <div className="p-3 bg-purple-500/20 text-purple-400 rounded-xl group-hover:bg-purple-500 group-hover:text-white transition-colors shadow-lg shadow-purple-500/10">
                                        <UserPlus size={24} />
                                    </div>
                                </div>
                                <h3 className="text-lg font-semibold text-white mb-1 relative z-10">Novo Cliente</h3>
                                <p className="text-sm text-gray-400 relative z-10">Cadastrar empresa</p>
                            </button>
                        </div>
                    </div>
                )}

                {activeTab === 'connection' && (
                    <div className="max-w-4xl mx-auto animate-fade-in">
                        <header className="mb-6 md:mb-8">
                            <h2 className="text-2xl md:text-3xl font-bold text-white">Conexão WhatsApp</h2>
                            <p className="text-gray-400 text-sm md:text-base">Escaneie o QR Code para conectar.</p>
                        </header>

                        <div className="bg-gray-800 rounded-2xl border border-gray-700 p-6 md:p-8 shadow-xl flex flex-col items-center text-center">
                            {connectionStatus.instance?.state === 'open' || connectionStatus.state === 'open' ? (
                                <div className="py-6 md:py-10">
                                    <div className="w-20 h-20 md:w-24 md:h-24 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-6 animate-bounce-slow">
                                        <CheckCircle2 size={40} className="text-emerald-500 md:w-12 md:h-12" />
                                    </div>
                                    <h3 className="text-xl md:text-2xl font-bold text-white mb-2">WhatsApp Conectado!</h3>
                                    <p className="text-gray-400 mb-8 text-sm md:text-base">O sistema está pronto para enviar e receber mensagens.</p>

                                    <button
                                        onClick={handleLogout}
                                        className="flex items-center gap-2 bg-red-600/10 hover:bg-red-600 text-red-500 hover:text-white px-6 py-3 rounded-xl transition-all font-medium border border-red-600/20 active:scale-95"
                                    >
                                        <LogOut size={18} />
                                        Desconectar
                                    </button>
                                </div>
                            ) : (
                                <div className="py-4 md:py-6 w-full">
                                    <div className="bg-white p-4 rounded-xl mb-6 inline-block shadow-lg">
                                        {qrCode ? (
                                            <img src={qrCode} alt="QR Code WhatsApp" className="w-56 h-56 md:w-64 md:h-64 object-contain" />
                                        ) : (
                                            <div className="w-56 h-56 md:w-64 md:h-64 flex items-center justify-center text-gray-400 bg-gray-100 rounded-lg">
                                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                                            </div>
                                        )}
                                    </div>
                                    <h3 className="text-lg md:text-xl font-bold text-white mb-2">Escaneie com seu celular</h3>
                                    <p className="text-gray-400 max-w-md mx-auto text-sm md:text-base">
                                        Abra o WhatsApp {'>'} Configurações {'>'} Aparelhos Conectados.
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {activeTab === 'clients' && (
                    <div className="max-w-5xl mx-auto animate-fade-in">
                        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
                            <div>
                                <h2 className="text-2xl md:text-3xl font-bold text-white">Meus Clientes</h2>
                                <p className="text-gray-400 text-sm md:text-base">Gerencie quem tem acesso.</p>
                            </div>
                            <button
                                onClick={() => setShowModal(true)}
                                className="w-full md:w-auto flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-xl transition-all shadow-lg shadow-emerald-900/20 font-medium active:scale-95"
                            >
                                <UserPlus size={20} />
                                Novo Cliente
                            </button>
                        </header>

                        <div className="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden shadow-xl">
                            <div className="p-4 md:p-6 border-b border-gray-700 bg-gray-800/50 sticky top-0 z-20 backdrop-blur-sm">
                                <div className="relative w-full">
                                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
                                    <input
                                        type="text"
                                        placeholder="Buscar cliente..."
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl pl-12 pr-4 py-3 text-gray-200 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all text-base"
                                    />
                                </div>
                            </div>

                            {/* Mobile List View */}
                            <div className="md:hidden divide-y divide-gray-700">
                                {loading ? (
                                    <div className="p-8 text-center text-gray-500">Carregando...</div>
                                ) : filteredClients.length === 0 ? (
                                    <div className="p-8 text-center text-gray-500">Nenhum cliente encontrado.</div>
                                ) : filteredClients.map((client) => (
                                    <div key={client.id} className="p-4 active:bg-gray-700/50 transition-colors">
                                        <div className="flex justify-between items-start mb-2">
                                            <div>
                                                <h3 className="font-bold text-white text-lg">{client.nome}</h3>
                                                <p className="text-emerald-400 text-sm font-medium">{client.empresa_nome}</p>
                                            </div>
                                            <button
                                                onClick={() => handleDelete(client.id)}
                                                className="text-gray-500 hover:text-red-400 p-2"
                                            >
                                                <Trash2 size={20} />
                                            </button>
                                        </div>
                                        <div className="flex flex-col gap-1 text-sm text-gray-400 font-mono">
                                            <p>📞 {client.telefone}</p>
                                            <p>🆔 {client.cnpj_cpf}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Desktop Table View */}
                            <div className="hidden md:block overflow-x-auto">
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
                        <header className="mb-6 md:mb-8">
                            <h2 className="text-2xl md:text-3xl font-bold text-white">Inteligência da Ana</h2>
                            <p className="text-gray-400 text-sm md:text-base">Configure o comportamento da IA.</p>
                        </header>

                        <div className="bg-gray-800 rounded-2xl border border-gray-700 p-4 md:p-8 shadow-xl">
                            <div className="flex items-start gap-4 md:gap-6 mb-6 md:mb-8">
                                <div className="p-3 md:p-4 bg-emerald-500/10 rounded-xl">
                                    <MessageSquare size={24} className="text-emerald-500 md:w-8 md:h-8" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="text-lg md:text-xl font-bold text-white mb-1 md:mb-2">Personalidade</h3>
                                    <p className="text-gray-400 text-xs md:text-sm leading-relaxed">
                                        Defina como a Ana deve falar e quais regras seguir.
                                    </p>
                                </div>
                            </div>

                            <div className="mb-6 md:mb-8">
                                <label className="block text-xs md:text-sm font-medium text-gray-300 mb-2 md:mb-3 uppercase tracking-wider">Instruções do Sistema</label>
                                <div className="relative">
                                    <textarea
                                        value={settings.system_prompt}
                                        onChange={(e) => setSettings({ ...settings, system_prompt: e.target.value })}
                                        className="w-full h-64 md:h-96 bg-gray-900 border border-gray-700 rounded-xl p-4 md:p-6 text-gray-300 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none font-mono text-sm leading-relaxed resize-none shadow-inner"
                                        placeholder="Ex: Você é uma assistente contábil..."
                                    />
                                </div>
                            </div>

                            <div className="flex items-center justify-end pt-6 border-t border-gray-700">
                                <button
                                    onClick={handleSaveSettings}
                                    className="w-full md:w-auto flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-8 py-3 rounded-xl transition-all shadow-lg shadow-emerald-900/20 font-bold active:scale-95"
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
                    <div className="fixed inset-0 bg-black/80 flex items-end md:items-center justify-center p-0 md:p-4 backdrop-blur-sm z-[70] animate-fade-in">
                        <div className="bg-gray-800 rounded-t-2xl md:rounded-2xl p-6 md:p-8 w-full max-w-md border-t md:border border-gray-700 shadow-2xl transform transition-all animate-slide-up md:animate-none">
                            <div className="flex justify-between items-center mb-6">
                                <h3 className="text-2xl font-bold text-white">Novo Cliente</h3>
                                <button onClick={() => setShowModal(false)} className="text-gray-400 hover:text-white p-2">
                                    <X size={24} />
                                </button>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-4 md:space-y-5">
                                <div>
                                    <label className="block text-sm font-medium text-gray-400 mb-1.5">Nome Completo</label>
                                    <input
                                        required
                                        value={formData.nome}
                                        onChange={e => setFormData({ ...formData, nome: e.target.value })}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all text-base"
                                        placeholder="Ex: João Silva"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-400 mb-1.5">Nome da Empresa</label>
                                    <input
                                        required
                                        value={formData.empresa_nome}
                                        onChange={e => setFormData({ ...formData, empresa_nome: e.target.value })}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all text-base"
                                        placeholder="Ex: Silva LTDA"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-400 mb-1.5">WhatsApp (com DDD)</label>
                                    <input
                                        required
                                        type="tel"
                                        placeholder="Ex: 5511999999999"
                                        value={formData.telefone}
                                        onChange={e => setFormData({ ...formData, telefone: e.target.value })}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all text-base"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-400 mb-1.5">CNPJ ou CPF</label>
                                    <input
                                        required
                                        value={formData.cnpj_cpf}
                                        onChange={e => setFormData({ ...formData, cnpj_cpf: e.target.value })}
                                        className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all text-base"
                                        placeholder="00.000.000/0001-00"
                                    />
                                </div>
                                <div className="flex gap-3 mt-8 pt-4">
                                    <button
                                        type="button"
                                        onClick={() => setShowModal(false)}
                                        className="flex-1 px-6 py-3 text-gray-400 hover:text-white font-medium transition-colors active:scale-95"
                                    >
                                        Cancelar
                                    </button>
                                    <button
                                        type="submit"
                                        className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-xl font-bold shadow-lg shadow-emerald-900/20 transition-all active:scale-95"
                                    >
                                        Salvar
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
