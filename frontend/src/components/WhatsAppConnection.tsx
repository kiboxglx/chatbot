import { useState, useEffect } from 'react';
import axios from 'axios';
import { QrCode, RefreshCw, Power, Smartphone, CheckCircle2 } from 'lucide-react';

// Use a URL do seu backend no Railway (que você mostrou na imagem)
const API_URL = '/api';

export default function WhatsAppConnection() {
    const [status, setStatus] = useState<'open' | 'close' | 'connecting'>('close');
    const [qrCode, setQrCode] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [instanceName] = useState('chatbot');

    // Pairing Code States
    const [pairingMode, setPairingMode] = useState(false);
    const [phoneNumber, setPhoneNumber] = useState('');
    const [pairingCode, setPairingCode] = useState<string | null>(null);

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
            const currentState = res.data.instance?.state || res.data.state || 'close';
            setStatus(currentState);

            if (currentState === 'open') {
                setQrCode(null);
                setPairingCode(null);
                setPairingMode(false);
            }
        } catch (error) {
            console.error("Erro ao verificar status:", error);
        }
    };

    const handleConnect = async () => {
        setLoading(true);
        setQrCode(null);
        setPairingCode(null);
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

    const handlePairingCode = async () => {
        if (!phoneNumber) {
            alert("Por favor, digite o número do telefone (ex: 5511999999999)");
            return;
        }
        setLoading(true);
        setPairingCode(null);
        try {
            // Aumenta timeout do frontend para 130s (2m10s)
            const res = await axios.post(`${API_URL}/management/pairing-code`, { number: phoneNumber }, { timeout: 130000 });
            if (res.data.pairingCode) {
                setPairingCode(res.data.pairingCode);
                setStatus('connecting');
            } else {
                alert("Não foi possível obter o código. Tente novamente.");
            }
        } catch (error: any) {
            console.error("Erro pairing:", error);
            alert(`Erro: ${error.response?.data?.detail || "Falha ao gerar código de pareamento"}`);
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
            setPairingCode(null);
            setPairingMode(false);
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
                    <h2 className="font-bold text-lg">Conexão WhatsApp</h2>
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
                        {!qrCode && !pairingCode ? (
                            <>
                                {!pairingMode ? (
                                    <>
                                        <div className="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                            <QrCode className="w-10 h-10 text-slate-400" />
                                        </div>
                                        <p className="text-gray-600 mb-8">Clique abaixo para gerar um novo QR Code e conectar o número do escritório.</p>
                                        <button
                                            onClick={handleConnect}
                                            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg shadow-blue-500/30 transition-all active:scale-95 flex items-center justify-center gap-2 mb-4"
                                        >
                                            <QrCode size={20} />
                                            Gerar QR Code
                                        </button>

                                        <button
                                            onClick={() => setPairingMode(true)}
                                            className="text-blue-600 hover:text-blue-800 text-sm font-medium underline"
                                        >
                                            Problemas com a câmera? Usar Código de Pareamento
                                        </button>
                                    </>
                                ) : (
                                    <div className="w-full animate-fade-in">
                                        <div className="mb-6 text-left">
                                            <label className="block text-sm font-medium text-gray-700 mb-2">Número do WhatsApp (com DDD)</label>
                                            <input
                                                type="text"
                                                placeholder="Ex: 5511999999999"
                                                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                                value={phoneNumber}
                                                onChange={(e) => setPhoneNumber(e.target.value)}
                                            />
                                            <p className="text-xs text-gray-500 mt-1">Digite apenas números, incluindo o código do país (55).</p>
                                        </div>

                                        <button
                                            onClick={handlePairingCode}
                                            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg shadow-blue-500/30 transition-all active:scale-95 flex items-center justify-center gap-2 mb-4"
                                        >
                                            Gerar Código
                                        </button>

                                        <button
                                            onClick={() => setPairingMode(false)}
                                            className="text-gray-500 hover:text-gray-700 text-sm"
                                        >
                                            Voltar para QR Code
                                        </button>
                                    </div>
                                )}
                            </>
                        ) : qrCode ? (
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
                        ) : (
                            <div className="flex flex-col items-center animate-fade-in">
                                <h3 className="text-lg font-bold text-gray-800 mb-4">Código de Pareamento</h3>
                                <div className="bg-slate-100 p-6 rounded-xl mb-6 w-full">
                                    <div className="text-4xl font-mono font-bold text-center tracking-widest text-slate-800 select-all cursor-pointer" onClick={() => navigator.clipboard.writeText(pairingCode || "")}>
                                        {pairingCode}
                                    </div>
                                </div>

                                <div className="text-left text-sm text-gray-600 bg-blue-50 p-4 rounded-lg mb-6">
                                    <p className="font-bold mb-2">Como conectar:</p>
                                    <ol className="list-decimal pl-4 space-y-1">
                                        <li>Abra o WhatsApp no celular</li>
                                        <li>Vá em <b>Configurações</b> {'>'} <b>Aparelhos conectados</b></li>
                                        <li>Toque em <b>Conectar um aparelho</b></li>
                                        <li>Toque em <b>Conectar com número de telefone</b></li>
                                        <li>Digite o código acima</li>
                                    </ol>
                                </div>

                                <button
                                    onClick={() => { setPairingCode(null); setPairingMode(false); }}
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
