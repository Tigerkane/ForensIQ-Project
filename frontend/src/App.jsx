import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [intelligence, setIntelligence] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const processEvidence = async () => {
    if (!file) {
        setError("Please select a file first.");
        return;
    }
    setError("");
    setLoading(true);
    setIntelligence(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/process", {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) throw new Error("Processing failed. Make sure backend is running.");
      
      const data = await response.json();
      setIntelligence(data.structured_intelligence);
    } catch (err) {
      setError(err.message || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 font-sans">
      <header className="mb-8 border-b border-gray-700 pb-4 flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold text-blue-400">ForensIQ</h1>
          <p className="text-gray-400 mt-1">Offline Investigation Intelligence</p>
        </div>
        <div className="flex items-center space-x-2 text-green-400">
          <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse"></div>
          <span className="text-sm font-semibold tracking-wider">OFFLINE MODE ACTIVE</span>
        </div>
      </header>
      
      <main className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-700">
          <h2 className="text-xl font-semibold mb-4 text-gray-200">Evidence Ingestion</h2>
          <div className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center hover:border-blue-400 transition-colors bg-gray-700/30">
            <input type="file" onChange={handleFileChange} className="w-full text-gray-400" />
            <p className="text-xs text-gray-500 mt-2">Supports PDF, Image, Audio</p>
          </div>
          {error && <p className="text-red-400 mt-2 text-sm">{error}</p>}
          <button 
            onClick={processEvidence}
            disabled={loading}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 py-3 rounded-lg text-white font-medium transition-colors shadow-lg shadow-blue-900/50"
          >
            {loading ? "Processing via Local AI..." : "Extract Intelligence"}
          </button>
        </div>
        
        <div className="md:col-span-2 bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-700 h-[600px] overflow-y-auto">
          <h2 className="text-xl font-semibold mb-4 text-gray-200">Structured Intelligence</h2>
          
          {!intelligence && !loading && (
            <div className="h-64 flex items-center justify-center border border-gray-700 rounded-lg bg-gray-900/50">
              <p className="text-gray-500 italic">Upload evidence to build the timeline.</p>
            </div>
          )}
          
          {loading && (
             <div className="h-64 flex flex-col items-center justify-center border border-gray-700 rounded-lg bg-gray-900/50">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mb-4"></div>
                <p className="text-blue-400 animate-pulse">Running CPU Inference (llama.cpp)...</p>
             </div>
          )}

          {intelligence && (
            <div className="space-y-6">
              <div className="bg-gray-900 p-4 rounded-lg border border-gray-700">
                <h3 className="text-lg font-bold text-green-400 mb-2">Entities Discovered</h3>
                <ul className="list-disc pl-5 text-gray-300">
                  {intelligence.people?.map((p, i) => (
                    <li key={i}><span className="font-semibold text-white">{p.name}</span> - {p.role}</li>
                  ))}
                </ul>
              </div>
              
              <div className="bg-gray-900 p-4 rounded-lg border border-gray-700">
                <h3 className="text-lg font-bold text-purple-400 mb-2">Investigation Events</h3>
                <div className="border-l-2 border-purple-500 pl-4 space-y-4">
                  {intelligence.events?.map((e, i) => (
                    <div key={i} className="mb-2">
                      <p className="text-sm text-purple-300">{e.time} @ {e.location}</p>
                      <p className="text-gray-200">{e.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App;
