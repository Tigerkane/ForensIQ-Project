import React, { useState, useEffect } from 'react';

function App() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState("Analyzing Evidence...");
  const [intelligence, setIntelligence] = useState(null);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("timeline");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [selectedModel, setSelectedModel] = useState("llama3.2");
  
  const [loadingStage, setLoadingStage] = useState(0);
  const [loadingSeconds, setLoadingSeconds] = useState(0);

  useEffect(() => {
    let timer;
    let stageTimer;
    if (loading) {
      setLoadingSeconds(0);
      setLoadingStage(0);
      timer = setInterval(() => setLoadingSeconds(s => s + 1), 1000);
      stageTimer = setInterval(() => setLoadingStage(s => Math.min(s + 1, 5)), 20000); // Change text every 20s
    }
    return () => {
      clearInterval(timer);
      clearInterval(stageTimer);
    };
  }, [loading]);

  const loadingMessages = [
    "Initializing offline AI model...",
    "Parsing and structuring evidence...",
    "Extracting critical entities and timelines...",
    "Building relationship knowledge graph...",
    "Evaluating risk scores and suspect profiles...",
    "Deep inference in progress (This can take 5-10 minutes on CPU)..."
  ];

  const handleFileChange = (e) => setFiles(Array.from(e.target.files));

  const handleDragOver = (e) => { e.preventDefault(); setIsDragging(true); };
  const handleDragLeave = (e) => { e.preventDefault(); setIsDragging(false); };
  const handleDrop = (e) => {
    e.preventDefault(); setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFiles(Array.from(e.dataTransfer.files));
    }
  };

  const processEvidence = async () => {
    if (files.length === 0) return setError("Please select files first.");
    setError(""); setLoading(true); setIntelligence(null);
    setActiveTab("timeline");
    
    try {
      let lastData = null;
      for (let i = 0; i < files.length; i++) {
        setLoadingText(`Processing file ${i + 1} of ${files.length}: ${files[i].name}... (this may take a few minutes on CPU)`);
        const formData = new FormData(); 
        formData.append("file", files[i]);
        formData.append("model", selectedModel);
        
        const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
        const response = await fetch(`${apiUrl}/process`, { 
          method: "POST", 
          body: formData,
          headers: {
            "ngrok-skip-browser-warning": "true"
          }
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Processing failed for ${files[i].name}: ${errText}`);
        }
        const data = await response.json();
        lastData = data;
      }
      
      if (lastData) {
        setLoading(false);
        if (!lastData.structured_intelligence || Object.keys(lastData.structured_intelligence).length === 0) {
          setError("Extraction failed. The AI returned incomplete data. Please check the backend logs.");
          setIntelligence(null);
        } else {
          setIntelligence(lastData.structured_intelligence);
          setActiveTab("timeline");
        }
      }
    } catch (err) { 
      setLoading(false);
      setError(err.message || "An error occurred."); 
    }
  };


  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery) return setSearchResults(null);
    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
      const response = await fetch(`${apiUrl}/search?query=${searchQuery}`, {
        headers: {
          "ngrok-skip-browser-warning": "true"
        }
      });
      setSearchResults(await response.json());
    } catch (err) { console.error(err); }
  };

  const handleDownloadReport = () => {
    if (!intelligence) return;
    let report = "=== FORENSIQ INTELLIGENCE REPORT ===\n\n";
    
    if (intelligence.executive_summary) {
      report += "EXECUTIVE SUMMARY:\n" + intelligence.executive_summary + "\n\n";
    }
    
    if (intelligence.risk_analysis) {
      report += `RISK ANALYSIS: ${intelligence.risk_analysis.score}/10 (Confidence: ${Math.round(intelligence.risk_analysis.confidence*100)}%)\n`;
      if (intelligence.risk_analysis.reasoning) {
        report += "Reasoning: " + (Array.isArray(intelligence.risk_analysis.reasoning) ? intelligence.risk_analysis.reasoning.join("; ") : intelligence.risk_analysis.reasoning) + "\n";
      }
      report += "\n";
    }
    
    if (intelligence.primary_suspect && intelligence.primary_suspect.entity) {
      report += `PRIMARY SUSPECT: ${intelligence.primary_suspect.entity}\n`;
      if (intelligence.primary_suspect.reasoning) {
        report += "Reasoning: " + (Array.isArray(intelligence.primary_suspect.reasoning) ? intelligence.primary_suspect.reasoning.join("; ") : intelligence.primary_suspect.reasoning) + "\n";
      }
      report += "\n";
    }

    if (intelligence.investigation_insights && intelligence.investigation_insights.length > 0) {
      report += "INVESTIGATION INSIGHTS:\n";
      intelligence.investigation_insights.forEach(i => report += `- ${i}\n`);
      report += "\n";
    }

    if (intelligence.recommended_actions && intelligence.recommended_actions.length > 0) {
      report += "RECOMMENDED ACTIONS:\n";
      intelligence.recommended_actions.forEach(a => report += `- ${a}\n`);
      report += "\n";
    }

    if (intelligence.people && intelligence.people.length > 0) {
      report += "PEOPLE INVOLVED:\n";
      intelligence.people.forEach(p => report += `- ${p.name} (${p.role})\n`);
      report += "\n";
    }

    if (intelligence.organizations && intelligence.organizations.length > 0) {
      report += "ORGANIZATIONS:\n";
      intelligence.organizations.forEach(o => report += `- ${o.name}\n`);
      report += "\n";
    }

    if (intelligence.evidence && intelligence.evidence.length > 0) {
      report += "PHYSICAL/DIGITAL EVIDENCE:\n";
      intelligence.evidence.forEach(e => {
        report += `- ${e.type}: ${e.description}\n`;
        report += `  Importance: ${e.importance} | Linked to: ${e.linked_people || 'N/A'}\n`;
      });
      report += "\n";
    }

    if (intelligence.weapons && intelligence.weapons.length > 0) {
      report += "WEAPONS RECOVERED:\n";
      intelligence.weapons.forEach(w => report += `- ${w.type}: ${w.description}\n`);
      report += "\n";
    }
    
    if (intelligence.vehicles && intelligence.vehicles.length > 0) {
      report += "VEHICLES:\n";
      intelligence.vehicles.forEach(v => report += `- ${v.model} (${v.registration})\n`);
      report += "\n";
    }

    if (intelligence.relationships && intelligence.relationships.length > 0) {
      report += "RELATIONSHIP GRAPH:\n";
      intelligence.relationships.forEach(r => report += `- [${r.source_entity}] --(${r.relationship_type})--> [${r.target_entity}]\n`);
      report += "\n";
    }

    if (intelligence.contradictions && intelligence.contradictions.length > 0) {
      report += "CONTRADICTIONS & CONFLICTING EVIDENCE:\n";
      intelligence.contradictions.forEach(c => report += `- ${c.description}\n`);
      report += "\n";
    }
    
    report += "--- TIMELINE OF EVENTS ---\n";
    (intelligence.timeline || []).forEach(e => {
      report += `[${e.timestamp || "Unknown Time"}] ${e.title || "Event"}\n`;
      if (e.location) report += `Location: ${e.location}\n`;
      if (e.description) report += `${e.description}\n`;
      report += "\n";
    });

    const blob = new Blob([report], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "ForensIQ_Report.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const currentData = intelligence;
  const eventsList = currentData?.timeline || [];

  const uploadBox = (
    <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl max-w-md mx-auto w-full">
      <h2 className="text-lg font-semibold mb-4 text-gray-200">Evidence Upload</h2>
      <div className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${isDragging ? 'border-blue-500 bg-blue-900/20 scale-105' : 'border-gray-700 bg-gray-950 hover:border-blue-500'}`} onDragOver={handleDragOver} onDragLeave={handleDragLeave} onDrop={handleDrop} onClick={() => document.getElementById('fileUpload').click()}>
        <input id="fileUpload" type="file" multiple onChange={handleFileChange} className="hidden" />
        <svg className={`w-16 h-16 mx-auto mb-4 transition-colors ${isDragging ? 'text-blue-500' : 'text-gray-600'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
        <p className="text-base font-medium text-gray-300">{files.length > 0 ? <span className="text-blue-500 font-bold">{files.length} File(s) Ready</span> : "Drag & Drop Evidence"}</p>
        {files.length > 0 && <p className="text-sm text-gray-500 mt-2">{files.map(f => f.name).join(', ')}</p>}
      </div>
      {error && <p className="text-red-400 mt-3 text-sm">{error}</p>}
      
      <div className="mt-4">
        <label className="block text-xs font-bold text-gray-400 uppercase mb-2">Intelligence Model</label>
        <select 
          value={selectedModel} 
          onChange={(e) => setSelectedModel(e.target.value)}
          className="w-full bg-gray-950 border border-gray-700 text-gray-200 rounded-lg p-3 text-sm font-medium focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all cursor-pointer"
        >
          <option value="llama3.2">Llama 3.2 (Fast & Smart)</option>
          <option value="qwen2.5:3b">Qwen 2.5 (Fast, Lower Accuracy)</option>
        </select>
      </div>
      <button onClick={processEvidence} disabled={loading || files.length === 0} className="mt-6 w-full bg-blue-600 hover:bg-blue-500 disabled:bg-gray-800 disabled:text-gray-500 py-4 rounded-lg text-base font-bold transition-colors shadow-blue-900/20 shadow-lg">
        {loading ? "Inference Running..." : "Extract Intelligence"}
      </button>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6 font-sans">
      <header className="mb-6 flex justify-between items-end border-b border-gray-800 pb-4">
        <div><h1 className="text-3xl font-bold text-blue-500">ForensIQ</h1><p className="text-sm text-gray-400">Offline Investigation Intelligence Platform</p></div>
        
        <form onSubmit={handleSearch} className="flex-1 max-w-md mx-8 relative">
           <input type="text" placeholder="Search global database..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="w-full bg-gray-900 border border-gray-700 rounded-full py-2 px-4 text-sm focus:outline-none focus:border-blue-500 text-gray-200" />
        </form>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-green-500"><div className="w-3 h-3 rounded-full bg-green-500 animate-pulse"></div><span className="text-xs font-bold tracking-wider">OFFLINE AI RUNNING</span></div>
        </div>
      </header>
      
      {searchResults && (
        <div className="mb-6 bg-blue-900/20 border border-blue-500/50 p-6 rounded-xl shadow-lg">
          <div className="flex justify-between items-center mb-4"><h2 className="text-lg font-bold text-blue-400">Global Database Search Results</h2><button onClick={() => setSearchResults(null)} className="text-gray-400 hover:text-white">Close</button></div>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div><h3 className="text-green-400 font-semibold border-b border-gray-700 pb-1 mb-2">People</h3>{searchResults.people.map(p => <div key={p.person_id}>{p.name}</div>)}</div>
            <div><h3 className="text-purple-400 font-semibold border-b border-gray-700 pb-1 mb-2">Vehicles</h3>{searchResults.vehicles.map(v => <div key={v.vehicle_id}>{v.registration}</div>)}</div>
            <div><h3 className="text-yellow-400 font-semibold border-b border-gray-700 pb-1 mb-2">Events</h3>{searchResults.events.map(e => <div key={e.event_id} className="truncate">{e.description}</div>)}</div>
          </div>
        </div>
      )}

      {loading ? (
        <main className="flex flex-col items-center justify-center min-h-[70vh]">
          <div className="bg-gray-900 border border-blue-500/30 p-10 rounded-2xl shadow-2xl shadow-blue-900/20 max-w-lg w-full text-center">
            <div className="relative w-24 h-24 mx-auto mb-8">
              <div className="absolute inset-0 border-4 border-blue-500/20 rounded-full"></div>
              <div className="absolute inset-0 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center text-blue-400 font-bold text-xl">
                {Math.floor(loadingSeconds / 60)}:{String(loadingSeconds % 60).padStart(2, '0')}
              </div>
            </div>
            
            <h2 className="text-2xl font-bold text-blue-400 mb-2">Analyzing Evidence</h2>
            
            <div className="h-12 flex items-center justify-center">
              <p className="text-gray-300 font-medium animate-pulse">
                {loadingMessages[loadingStage]}
              </p>
            </div>
            
            <div className="mt-8 bg-gray-950 p-4 rounded-lg border border-gray-800 text-left">
              <p className="text-xs text-gray-500 uppercase font-bold mb-1">Active Model</p>
              <p className="text-sm text-blue-400 font-mono">{selectedModel}</p>
              <p className="text-xs text-gray-600 mt-2">Running locally on CPU. 100% offline & secure.</p>
            </div>
          </div>
        </main>
      ) : (!intelligence) ? (
        <main className="flex flex-col items-center justify-center min-h-[70vh]">
          {uploadBox}
        </main>
      ) : (
        <main className="grid grid-cols-1 xl:grid-cols-4 gap-6">
          <div className="xl:col-span-1 space-y-3">
            {uploadBox}
            
            {intelligence && intelligence.risk_analysis && (
              <div className="bg-gray-900 border border-orange-500/50 p-4 rounded-xl shadow-lg">
                <h3 className="text-orange-400 font-bold text-sm mb-2">Case Risk Score</h3>
                <div className="w-full bg-gray-800 rounded-full h-2 mt-1 mb-2">
                  <div className="bg-orange-500 h-2 rounded-full" style={{width: `${(intelligence.risk_analysis.score/10)*100}%`}}></div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-orange-200/50">Conf: {Math.round(intelligence.risk_analysis.confidence*100)}%</span>
                  <span className="text-xs text-orange-300 font-bold">{intelligence.risk_analysis.score} / 10</span>
                </div>
              </div>
            )}
            
            {intelligence && intelligence.primary_suspect && intelligence.primary_suspect.entity && (
              <div className="bg-gray-900 border border-yellow-500/50 p-4 rounded-xl shadow-lg">
                <h3 className="text-yellow-400 font-bold text-sm mb-2">Primary Suspect</h3>
                <div className="flex justify-between items-end">
                  <p className="text-lg text-yellow-100 font-bold truncate">{intelligence.primary_suspect.entity}</p>
                  <span className="text-xs text-yellow-300/70 whitespace-nowrap ml-2">{Math.round(intelligence.primary_suspect.confidence*100)}% sure</span>
                </div>
              </div>
            )}
            
            {intelligence && (
              <div className="flex flex-col space-y-3 mt-4">
                <button onClick={() => setIsModalOpen(true)} className="w-full py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 font-bold rounded-lg border border-gray-700 transition-colors shadow-lg">
                  View Other Sections
                </button>
                <button onClick={handleDownloadReport} className="w-full py-3 flex items-center justify-center space-x-2 bg-blue-900/30 hover:bg-blue-800/40 text-blue-400 font-bold rounded-lg border border-blue-800/50 transition-colors shadow-lg">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                  <span>Download Report (.txt)</span>
                </button>
              </div>
            )}
          </div>
          
          <div className="xl:col-span-3 bg-gray-900 rounded-xl border border-gray-800 flex flex-col h-[900px] shadow-lg relative">
          
          <div className="flex border-b border-gray-800 bg-gray-950 rounded-t-xl overflow-hidden">
            {['timeline', 'entities', 'relationships'].map(tab => (
              <button key={tab} onClick={() => setActiveTab(tab)} className={`flex-1 py-4 text-sm font-bold capitalize transition-colors ${activeTab === tab ? 'bg-gray-800 text-blue-500 border-b-2 border-blue-500' : 'text-gray-500 hover:bg-gray-800/50'}`}>
                {tab}
              </button>
            ))}
          </div>
          
          <div className="p-6 overflow-y-auto flex-1 relative custom-scrollbar">
            {!currentData && !loading && <div className="h-full flex items-center justify-center"><p className="text-gray-600 italic">Upload an investigation file or view Master Database.</p></div>}
            {loading && <div className="h-full flex flex-col items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div><p className="text-blue-500 animate-pulse font-medium">{loadingText}</p></div>}
            
            {/* Summary tab removed */}

            {intelligence && activeTab === 'timeline' && intelligence.executive_summary && (
              <div className="mb-6 bg-gray-800 p-5 rounded-lg border border-gray-700 shadow-md">
                <h3 className="text-blue-400 font-bold mb-2">Executive Intelligence Briefing</h3>
                <p className="text-gray-300 text-sm leading-relaxed">{intelligence.executive_summary}</p>
              </div>
            )}

            {(currentData && activeTab === 'timeline' && !loading) && (
              <div className="space-y-6 border-l-2 border-blue-900 pl-4 ml-4">
                {eventsList.map((e, i) => (
                  <div key={i} className="relative bg-gray-950 p-4 rounded-lg border border-gray-800 hover:border-gray-700 transition-colors">
                    <div className="absolute -left-[23px] top-4 w-3 h-3 bg-blue-500 rounded-full shadow-[0_0_10px_rgba(59,130,246,0.8)]"></div>
                    <div className="flex justify-between items-start mb-1">
                      <p className="text-xs font-bold text-blue-500 uppercase">{e.time || "Unknown"} | {e.location || "Unknown"}</p>
                      {e.confidence && <span className="text-[10px] text-blue-400/50">{Math.round(e.confidence*100)}% conf</span>}
                    </div>
                    {e.title && <p className="text-sm font-bold text-gray-100 mb-1">{e.title}</p>}
                    <p className="text-sm text-gray-300 mb-2">{e.description || e.event}</p>
                    {e.reasoning && <p className="text-xs text-blue-200/80 italic mb-2 border-l-2 border-blue-900/50 pl-2">{e.reasoning}</p>}
                    {(e.entities_involved || e.supporting_evidence) && (
                      <div className="flex flex-wrap gap-2 mt-2">
                        {e.entities_involved && <span className="text-[10px] px-2 py-1 bg-green-900/20 text-green-400 border border-green-800/50 rounded-md">Entities: {e.entities_involved}</span>}
                        {e.supporting_evidence && <span className="text-[10px] px-2 py-1 bg-pink-900/20 text-pink-400 border border-pink-800/50 rounded-md">Evidence: {e.supporting_evidence}</span>}
                      </div>
                    )}
                  </div>
                ))}
                {eventsList.length === 0 && <p className="text-gray-500 italic">No events found.</p>}
              </div>
            )}
            
            {(currentData && activeTab === 'entities' && !loading) && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-950 p-5 rounded-lg border border-gray-800"><h3 className="text-sm font-bold text-green-500 mb-3 border-b border-gray-800 pb-2">People</h3><ul className="text-xs space-y-2">{currentData.people?.map((p, i) => <li key={i} className="flex justify-between items-center"><span className="text-white font-semibold">{p.name}</span> <div className="flex gap-2"><span className="text-gray-400 bg-gray-900 px-2 rounded">{p.role}</span>{p.confidence && <span className="text-green-400 bg-green-900/20 px-1 rounded">{Math.round(p.confidence*100)}%</span>}</div></li>)}</ul></div>
                <div className="bg-gray-950 p-5 rounded-lg border border-gray-800"><h3 className="text-sm font-bold text-yellow-500 mb-3 border-b border-gray-800 pb-2">Organizations</h3><ul className="text-xs space-y-2">{currentData.organizations?.map((o, i) => <li key={i} className="flex justify-between items-center"><span className="text-white font-medium">{o.name}</span>{o.confidence && <span className="text-yellow-400 bg-yellow-900/20 px-1 rounded">{Math.round(o.confidence*100)}%</span>}</li>)}</ul></div>
                <div className="bg-gray-950 p-5 rounded-lg border border-gray-800"><h3 className="text-sm font-bold text-purple-500 mb-3 border-b border-gray-800 pb-2">Vehicles</h3><ul className="text-xs space-y-2">{currentData.vehicles?.map((v, i) => <li key={i} className="flex justify-between items-center"><div><span className="text-white font-semibold">{v.registration}</span> - {v.model}</div>{v.confidence && <span className="text-purple-400 bg-purple-900/20 px-1 rounded">{Math.round(v.confidence*100)}%</span>}</li>)}</ul></div>
                <div className="bg-gray-950 p-5 rounded-lg border border-gray-800"><h3 className="text-sm font-bold text-red-500 mb-3 border-b border-gray-800 pb-2">Weapons</h3><ul className="text-xs space-y-2">{currentData.weapons?.map((w, i) => <li key={i} className="flex flex-col gap-1 border-b border-gray-800/50 pb-2"><div className="flex justify-between items-center"><span className="text-red-400 font-bold">[{w.type}]</span> {w.confidence && <span className="text-red-400 bg-red-900/20 px-1 rounded">{Math.round(w.confidence*100)}%</span>}</div><span className="text-gray-300">{w.description}</span></li>)}</ul></div>
                <div className="bg-gray-950 p-5 rounded-lg border border-gray-800"><h3 className="text-sm font-bold text-pink-500 mb-3 border-b border-gray-800 pb-2">Evidence</h3><ul className="text-xs space-y-3">{currentData.evidence?.map((ev, i) => <li key={i} className="flex flex-col gap-1 border-b border-gray-800/50 pb-2"><div className="flex justify-between items-center"><span className="text-pink-400 font-bold">[{ev.type}]</span> {ev.confidence && <span className="text-[10px] text-pink-500/50">{Math.round(ev.confidence*100)}% conf</span>}</div><span className="text-gray-300">{ev.description}</span>{ev.reasoning && <span className="text-[10px] text-pink-200/70 italic mt-1">{ev.reasoning}</span>}<div className="flex flex-wrap gap-2 mt-1">{ev.importance && <span className={`text-[10px] px-2 py-0.5 rounded ${ev.importance==='Critical'?'bg-red-700/50 text-red-200': ev.importance==='High'?'bg-red-900/30 text-red-400': ev.importance==='Medium'?'bg-yellow-900/30 text-yellow-400':'bg-gray-800 text-gray-400'}`}>{ev.importance}</span>}{ev.linked_people && <span className="text-[10px] text-gray-400 bg-gray-900 px-2 py-0.5 rounded">People: {ev.linked_people}</span>}</div></li>)}</ul></div>
              </div>
            )}
            
            {(currentData && activeTab === 'relationships' && !loading) && (
              <div className="space-y-4 max-w-5xl mx-auto mt-4">
                {currentData.relationships?.map((r, i) => (
                  <div key={i} className="flex items-center justify-between bg-gray-950 p-4 rounded-xl border border-gray-800 shadow-md hover:border-gray-700 transition-colors">
                    <span className="text-blue-300 text-sm font-bold px-4 py-2 bg-blue-900/20 border border-blue-800/50 rounded-lg whitespace-nowrap">{r.entity1 || r.source_entity}</span>
                    <div className="flex-1 flex flex-col items-center px-4">
                        <span className="text-gray-400 text-xs tracking-widest uppercase mb-1 text-center">{r.relation || r.relationship || r.relationship_type}</span>
                        <div className="w-full flex items-center px-2">
                            <div className="h-px bg-gray-500 flex-1"></div>
                            <div className="w-0 h-0 border-t-[4px] border-t-transparent border-b-[4px] border-b-transparent border-l-[6px] border-l-gray-500"></div>
                        </div>
                        {r.confidence && <span className="text-[10px] text-gray-500 mt-1">{Math.round(r.confidence*100)}% conf {r.evidence_reference || r.supporting_evidence ? `• ${r.evidence_reference || r.supporting_evidence}`:''}</span>}
                        {r.reasoning && <span className="text-[10px] text-blue-200/70 italic mt-1 text-center max-w-[200px] leading-tight">{r.reasoning}</span>}
                    </div>
                    <span className="text-purple-300 text-sm font-bold px-4 py-2 bg-purple-900/20 border border-purple-800/50 rounded-lg whitespace-nowrap">{r.entity2 || r.target_entity}</span>
                  </div>
                ))}
                {(!currentData.relationships || currentData.relationships.length === 0) && <p className="text-center text-gray-500 mt-10">No relationships detected in this document.</p>}
              </div>
            )}


          </div>
        </div>
      </main>
    )}
    
    {/* ChatGPT-Style Modal Overlay */}
    {isModalOpen && intelligence && (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-6" onClick={() => setIsModalOpen(false)}>
        <div className="bg-gray-900 border border-gray-700 rounded-2xl w-full max-w-4xl max-h-[85vh] overflow-y-auto custom-scrollbar shadow-2xl relative" onClick={e => e.stopPropagation()}>
          <button onClick={() => setIsModalOpen(false)} className="absolute top-4 right-4 text-gray-400 hover:text-white bg-gray-800 hover:bg-gray-700 p-2 rounded-full transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
          
          <div className="p-8">
            <h2 className="text-2xl font-bold text-white mb-6 border-b border-gray-800 pb-4">Executive Intelligence Summary</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Left Column */}
              <div className="space-y-6">
                {intelligence.risk_analysis && (
                   <div className="bg-orange-900/20 border border-orange-500/50 p-6 rounded-xl shadow-lg">
                     <h3 className="text-orange-400 font-bold text-lg mb-3">Case Risk Score</h3>
                     <div className="w-full bg-gray-800 rounded-full h-4 mt-2 mb-2">
                       <div className="bg-orange-500 h-4 rounded-full" style={{width: `${(intelligence.risk_analysis.score/10)*100}%`}}></div>
                     </div>
                     <div className="flex justify-between items-center mb-4">
                       <span className="text-sm text-orange-200/50">Confidence: {Math.round(intelligence.risk_analysis.confidence*100)}%</span>
                       <span className="text-sm text-orange-300 font-bold">{intelligence.risk_analysis.score} / 10</span>
                     </div>
                     <ul className="text-sm text-orange-200 space-y-2">
                       {intelligence.risk_analysis.reasoning?.map((r, i) => <li key={i}>• {r}</li>)}
                     </ul>
                   </div>
                )}

                {intelligence.investigation_insights?.length > 0 && (
                   <div className="bg-cyan-900/20 border border-cyan-500/50 p-6 rounded-xl shadow-lg">
                     <h3 className="text-cyan-400 font-bold text-lg mb-4">Investigation Insights</h3>
                     <ul className="text-sm text-cyan-200 space-y-3">
                       {intelligence.investigation_insights.map((c, i) => <li key={i}>• {c}</li>)}
                     </ul>
                   </div>
                )}
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                {intelligence.primary_suspect && intelligence.primary_suspect.entity && (
                   <div className="bg-yellow-900/20 border border-yellow-500/50 p-6 rounded-xl shadow-lg">
                     <h3 className="text-yellow-400 font-bold text-lg mb-3">Primary Suspect</h3>
                     <div className="flex justify-between items-end mb-4">
                       <p className="text-2xl text-yellow-100 font-bold">{intelligence.primary_suspect.entity}</p>
                       <span className="text-sm text-yellow-300/70">{Math.round(intelligence.primary_suspect.confidence*100)}% sure</span>
                     </div>
                     <div className="space-y-4">
                       <div>
                         <p className="text-sm font-semibold text-yellow-500 mb-2">Reasoning:</p>
                         <ul className="text-sm text-yellow-200/80 space-y-2">
                           {intelligence.primary_suspect.reasoning?.map((r, i) => <li key={i}>- {r}</li>)}
                         </ul>
                       </div>
                       {intelligence.primary_suspect.supporting_evidence?.length > 0 && (
                       <div>
                         <p className="text-sm font-semibold text-yellow-500 mb-2">Key Evidence:</p>
                         <ul className="text-sm text-yellow-200/80 space-y-2">
                           {intelligence.primary_suspect.supporting_evidence?.map((r, i) => <li key={i}>- {r}</li>)}
                         </ul>
                       </div>
                       )}
                     </div>
                   </div>
                )}

                {intelligence.recommended_actions?.length > 0 && (
                   <div className="bg-green-900/20 border border-green-500/50 p-6 rounded-xl shadow-lg">
                     <h3 className="text-green-400 font-bold text-lg mb-4">Recommended Actions</h3>
                     <ul className="text-sm text-green-200 space-y-3">
                       {intelligence.recommended_actions.map((a, i) => (
                         <li key={i} className="flex gap-3">
                           <span className="text-green-500">→</span> <span>{a}</span>
                         </li>
                       ))}
                     </ul>
                   </div>
                )}
                
                {intelligence.contradictions?.length > 0 && (
                   <div className="bg-red-900/20 border border-red-500/50 p-6 rounded-xl shadow-lg">
                     <h3 className="text-red-400 font-bold text-lg mb-4">Contradictions Detected</h3>
                     <ul className="text-sm text-red-300 space-y-3">
                       {intelligence.contradictions.map((c, i) => <li key={i}>• {c.description}</li>)}
                     </ul>
                   </div>
                )}
              </div>
            </div>
            
          </div>
        </div>
      </div>
    )}
      <style>{`
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background-color: #374151; border-radius: 20px; }
      `}</style>
    </div>
  )
}
export default App;
