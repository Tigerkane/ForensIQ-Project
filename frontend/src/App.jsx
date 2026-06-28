import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [intelligence, setIntelligence] = useState(null);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("timeline"); 
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const processEvidence = async () => {
    if (!file) return setError("Please select a file first.");
    setError(""); setLoading(true); setIntelligence(null);
    const formData = new FormData(); formData.append("file", file);
    try {
      const response = await fetch("http://localhost:8000/api/process", { method: "POST", body: formData });
      if (!response.ok) throw new Error("Processing failed.");
      const data = await response.json();
      setIntelligence(data.structured_intelligence);
    } catch (err) { setError(err.message || "An error occurred."); } 
    finally { setLoading(false); }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery) { setSearchResults(null); return; }
    try {
      const response = await fetch(`http://localhost:8000/api/search?query=${searchQuery}`);
      const data = await response.json();
      setSearchResults(data);
    } catch (err) { console.error(err); }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 font-sans">
      <header className="mb-6 flex justify-between items-end border-b border-gray-700 pb-4">
        <div><h1 className="text-3xl font-bold text-blue-400">ForensIQ</h1><p className="text-sm text-gray-400">Offline Investigation Intelligence Platform</p></div>
        
        {/* Global Search Bar */}
        <form onSubmit={handleSearch} className="flex-1 max-w-md mx-8 relative">
           <input 
             type="text" 
             placeholder="Search database (People, Vehicles, Events)..." 
             value={searchQuery}
             onChange={(e) => setSearchQuery(e.target.value)}
             className="w-full bg-gray-800 border border-gray-600 rounded-full py-2 px-4 text-sm focus:outline-none focus:border-blue-500 text-gray-200"
           />
           <button type="submit" className="absolute right-3 top-2.5 text-gray-400 hover:text-blue-400">
             <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
           </button>
        </form>

        <div className="flex items-center space-x-2 text-green-400"><div className="w-3 h-3 rounded-full bg-green-400 animate-pulse"></div><span className="text-xs font-semibold tracking-wider">OFFLINE AI RUNNING</span></div>
      </header>
      
      {/* Search Results Overlay */}
      {searchResults && (
        <div className="mb-6 bg-blue-900/20 border border-blue-500/50 p-6 rounded-xl shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-bold text-blue-400">Global Database Search Results</h2>
            <button onClick={() => setSearchResults(null)} className="text-gray-400 hover:text-white">Close</button>
          </div>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div><h3 className="text-green-400 font-semibold border-b border-gray-700 pb-1 mb-2">People</h3>{searchResults.people.map(p => <div key={p.person_id}>{p.name} ({p.role})</div>)}</div>
            <div><h3 className="text-purple-400 font-semibold border-b border-gray-700 pb-1 mb-2">Vehicles</h3>{searchResults.vehicles.map(v => <div key={v.vehicle_id}>{v.registration} - {v.model}</div>)}</div>
            <div><h3 className="text-yellow-400 font-semibold border-b border-gray-700 pb-1 mb-2">Events</h3>{searchResults.events.map(e => <div key={e.event_id} className="truncate">{e.description}</div>)}</div>
          </div>
        </div>
      )}

      <main className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow-lg">
            <h2 className="text-lg font-semibold mb-3 text-gray-200">Evidence Upload</h2>
            
            <div 
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${isDragging ? 'border-blue-400 bg-blue-900/20 scale-105' : 'border-gray-600 bg-gray-900/50 hover:border-blue-400 hover:bg-gray-800'}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => document.getElementById('fileUpload').click()}
            >
              <input id="fileUpload" type="file" onChange={handleFileChange} className="hidden" />
              <svg className={`w-12 h-12 mx-auto mb-3 transition-colors ${isDragging ? 'text-blue-400' : 'text-gray-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
              <p className="text-sm font-medium text-gray-300">
                {file ? <span className="text-blue-400">{file.name}</span> : "Click or Drag & Drop Evidence"}
              </p>
              <p className="text-xs text-gray-500 mt-2">Supports PDF, Image, Audio</p>
            </div>
            
            {error && <p className="text-red-400 mt-2 text-xs">{error}</p>}
            <button onClick={processEvidence} disabled={loading || !file} className="mt-4 w-full bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-400 py-3 rounded-lg text-sm font-bold transition-colors shadow-blue-900/50 shadow-lg">
              {loading ? "Running Local Inference..." : "Extract Intelligence"}
            </button>
          </div>
          
          {intelligence?.root_cause && (
             <div className="bg-yellow-900/20 border border-yellow-500/50 p-4 rounded-xl shadow-lg mb-6">
               <h3 className="text-yellow-400 font-bold text-sm mb-2 flex items-center">
                 <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                 Primary Suspect / Root Cause
               </h3>
               <p className="text-sm text-yellow-100 font-bold">{intelligence.root_cause.entity_name}</p>
               <p className="text-xs text-yellow-300 mt-1">{intelligence.root_cause.reasoning}</p>
             </div>
          )}
          
          {intelligence?.contradictions?.length > 0 && (
             <div className="bg-red-900/20 border border-red-500/50 p-4 rounded-xl shadow-lg">
               <h3 className="text-red-400 font-bold text-sm mb-2 flex items-center">
                 <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                 AI Contradictions Detected
               </h3>
               <ul className="text-xs text-red-300 space-y-2">
                 {intelligence.contradictions.map((c, i) => <li key={i}>• {c.description}</li>)}
               </ul>
             </div>
          )}
        </div>
        
        <div className="lg:col-span-3 bg-gray-800 rounded-xl border border-gray-700 flex flex-col h-[700px] shadow-lg">
          <div className="flex border-b border-gray-700 bg-gray-900/30 rounded-t-xl">
            {['timeline', 'entities', 'relationships'].map(tab => (
              <button key={tab} onClick={() => setActiveTab(tab)} className={`flex-1 py-4 text-sm font-bold capitalize transition-colors ${activeTab === tab ? 'bg-gray-700 text-blue-400 border-b-2 border-blue-400' : 'text-gray-400 hover:bg-gray-700/50'}`}>
                {tab}
              </button>
            ))}
          </div>
          
          <div className="p-6 overflow-y-auto flex-1">
            {!intelligence && !loading && <div className="h-full flex items-center justify-center"><p className="text-gray-500 italic">Upload an investigation file to begin extraction.</p></div>}
            {loading && <div className="h-full flex flex-col items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div><p className="text-blue-400 animate-pulse text-sm">Building Knowledge Graph via Ollama...</p></div>}
            
            {intelligence && activeTab === 'timeline' && (
              <div className="space-y-6 border-l-2 border-blue-500/30 pl-4 ml-4 mt-2">
                {intelligence.events?.map((e, i) => (
                  <div key={i} className="relative bg-gray-900/50 p-4 rounded-lg border border-gray-700 hover:border-gray-500 transition-colors">
                    <div className="absolute -left-[23px] top-4 w-3 h-3 bg-blue-500 rounded-full shadow-[0_0_10px_rgba(59,130,246,0.8)]"></div>
                    <p className="text-xs font-bold text-blue-400 tracking-wider uppercase mb-1">{e.time || "Unknown Time"} | {e.location || "Unknown Location"}</p>
                    <p className="text-sm text-gray-200">{e.description}</p>
                  </div>
                ))}
              </div>
            )}
            
            {intelligence && activeTab === 'entities' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-900/80 p-5 rounded-lg border border-gray-700 shadow"><h3 className="text-sm font-bold text-green-400 mb-3 border-b border-gray-700 pb-2">People</h3><ul className="text-xs text-gray-300 space-y-2">{intelligence.people?.map((p, i) => <li key={i} className="flex justify-between"><span className="text-white font-semibold">{p.name}</span> <span className="text-gray-500 bg-gray-800 px-2 rounded">{p.role}</span></li>)}</ul></div>
                <div className="bg-gray-900/80 p-5 rounded-lg border border-gray-700 shadow"><h3 className="text-sm font-bold text-yellow-400 mb-3 border-b border-gray-700 pb-2">Organizations</h3><ul className="text-xs text-gray-300 space-y-2">{intelligence.organizations?.map((o, i) => <li key={i} className="text-white font-medium">{o.name}</li>)}</ul></div>
                <div className="bg-gray-900/80 p-5 rounded-lg border border-gray-700 shadow"><h3 className="text-sm font-bold text-purple-400 mb-3 border-b border-gray-700 pb-2">Vehicles</h3><ul className="text-xs text-gray-300 space-y-2">{intelligence.vehicles?.map((v, i) => <li key={i}><span className="text-white font-semibold">{v.registration}</span> - {v.model}</li>)}</ul></div>
                <div className="bg-gray-900/80 p-5 rounded-lg border border-gray-700 shadow"><h3 className="text-sm font-bold text-pink-400 mb-3 border-b border-gray-700 pb-2">Evidence & Weapons</h3><ul className="text-xs text-gray-300 space-y-2">
                  {intelligence.evidence?.map((ev, i) => <li key={i}><span className="text-pink-300 font-medium">[{ev.type}]</span> {ev.description}</li>)}
                  {intelligence.weapons?.map((w, i) => <li key={i}><span className="text-red-400 font-medium">[WEAPON]</span> {w.type}</li>)}
                </ul></div>
              </div>
            )}
            
            {intelligence && activeTab === 'relationships' && (
              <div className="space-y-4 max-w-2xl mx-auto mt-4">
                {intelligence.relationships?.map((r, i) => (
                  <div key={i} className="flex items-center justify-between bg-gray-900 p-4 rounded-xl border border-gray-700 shadow-md">
                    <span className="text-blue-300 text-sm font-bold px-4 py-2 bg-blue-900/20 border border-blue-800/50 rounded-lg whitespace-nowrap">{r.entity1}</span>
                    <div className="flex-1 flex flex-col items-center px-4">
                        <span className="text-gray-400 text-xs tracking-widest uppercase mb-1">{r.relation}</span>
                        <div className="w-full h-px bg-gradient-to-r from-transparent via-gray-500 to-transparent"></div>
                    </div>
                    <span className="text-purple-300 text-sm font-bold px-4 py-2 bg-purple-900/20 border border-purple-800/50 rounded-lg whitespace-nowrap">{r.entity2}</span>
                  </div>
                ))}
                {!intelligence.relationships?.length && <p className="text-center text-gray-500 mt-10">No explicit relationships detected in this document.</p>}
              </div>
            )}
            
          </div>
        </div>
      </main>
    </div>
  )
}
export default App;
