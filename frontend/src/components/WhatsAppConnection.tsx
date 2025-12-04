import { useState, useEffect } from 'react';
import axios from 'axios';
import { QrCode, RefreshCw, Power, Smartphone, CheckCircle2 } from 'lucide-react';

// Use a URL do seu backend no Railway (que você mostrou na imagem)
const API_URL = 'https://chatbot-production-e324.up.railway.app';

export default function WhatsAppConnection() {
    const [status, setStatus] = useState<'open' | 'close' | 'connecting'>('close');
    const [qrCode, setQrCode] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [instanceName] = useState('chatbot');

    // Verifica status ao carregar
    useEffect(() => {
        console.log("WhatsAppConnection V2 Loaded. API URL:", API_URL);
        checkStatus();
        const interval = setInterval(() => {
            if (status !== 'open') checkStatus();
        }, 5000); // Polling a cada 5s se não estiver conectado
        return () => clearInterval(interval);
    }, [status]);

    const checkStatus = async () => {
        try {
            const res = await axios.get(`${API_URL}/management/status`);
            // Ajuste conforme a resposta exata do seu endpoint management.py
            const currentState = res.data.instance?.state || res.data.state || 'close';
            setStatus(currentState);

            if (currentState === 'open') {
                setQrCode(null);
            }
        } catch (error) {
            console.error("Erro ao verificar status:", error);
        }
    };

    const handleConnect = async () => {
        setLoading(true);
        setQrCode(null);
        try {
            const res = await axios.get(`${API_URL}/management/qrcode`);
            if (res.data.base64) {
                setQrCode(res.data.base64);
                setStatus('connecting');
            } else if (res.data.code) {
                setQrCode(res.data.code);
                setStatus('connecting');
            }
        } catch (error: any) {
            console.error("Erro detalhado:", error.response?.data || error.message);
            alert(`Erro ao gerar QR Code: ${error.response?.data?.detail || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        if (!confirm("Tem certeza que deseja desconectar? O robô vai parar.")) return;
        setLoading(true);
        try {
            await axios.post(`${API_URL}/management/logout`);
            setStatus('close');
            setQrCode(null);
        } catch (error) {
            alert("Erro ao desconectar.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-full max-w-md mx-auto bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <div className="bg-slate-900 p-6 text-white flex justify-between items-center">
                <div className="flex items-center gap-3">
                    <Smartphone className="w-6 h-6 text-emerald-400" />
                    <h2 className="font-bold text-lg">Conexão WhatsApp (V2)</h2>
                </div>
                <div className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 ${status === 'open' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50' : 'bg-red-500/20 text-red-400 border border-red-500/50'
                    }`}>
                    {status === 'open' ? 'ONLINE' : 'OFFLINE'}
                </div>
            </div>

            <div className="p-8 flex flex-col items-center justify-center min-h-[300px]">
                {loading ? (
                    <div className="flex flex-col items-center animate-pulse">
                        <RefreshCw className="w-12 h-12 text-blue-500 animate-spin mb-4" />
                        <p className="text-gray-500">Processando...</p>
                    </div>
                ) : status === 'open' ? (
                    <div className="text-center animate-fade-in">
                        <div className="w-24 h-24 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6">
                            <CheckCircle2 className="w-12 h-12 text-emerald-600" />
                        </div>
                        <h3 className="text-xl font-bold text-gray-800 mb-2">Tudo Pronto!</h3>
                        <p className="text-gray-500 mb-8">Seu robô está conectado e respondendo mensagens na instância <b>{instanceName}</b>.</p>

                        <button
                            onClick={handleLogout}
                            className="flex items-center justify-center gap-2 w-full py-3 rounded-xl border-2 border-red-100 text-red-600 font-semibold hover:bg-red-50 transition-colors"
                        >
                            <Power size={20} />
                            Desconectar WhatsApp
                        </button>
                    </div>
                ) : (
                    <div className="text-center w-full animate-fade-in">
                        {!qrCode ? (
                            <>
                                <div className="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                    <QrCode className="w-10 h-10 text-slate-400" />
                                </div>
                                <p className="text-gray-600 mb-8">Clique abaixo para gerar um novo QR Code e conectar o número do escritório.</p>
                                <button
                                    onClick={handleConnect}
                                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg shadow-blue-500/30 transition-all active:scale-95 flex items-center justify-center gap-2"
                                >
                                    <QrCode size={20} />
                                    Gerar QR Code
                                </button>
                            </>
                        ) : (
                            <div className="flex flex-col items-center">
                                <p className="text-sm text-gray-500 mb-4 font-medium uppercase tracking-wide">Escaneie com seu celular</p>
                                <div className="p-2 border-4 border-slate-900 rounded-xl mb-6 shadow-2xl">
                                    <img src={qrCode} alt="QR Code WhatsApp" className="w-64 h-64 object-contain" />
                                </div>
                                <button
                                    onClick={() => setQrCode(null)}
                                    className="text-gray-400 hover:text-gray-600 text-sm underline"
                                >
                                    Cancelar / Tentar de novo
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
