import React, { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import NetworkScene from './components/NetworkScene'
import './index.css'

const API = 'http://localhost:8000/api'

export default function App() {
  const [activeTab, setActiveTab] = useState('01')
  
  // Data State
  const [network, setNetwork] = useState(null)
  const [stats, setStats] = useState(null)
  const [eigen, setEigen] = useState(null)
  const [matrices, setMatrices] = useState(null)
  const [clusterData, setClusterData] = useState(null)
  const [centrality, setCentrality] = useState(null)
  const [pathData, setPathData] = useState(null)
  
  // UI State
  const [hovered, setHovered] = useState(null)
  const [k, setK] = useState(2)
  const [loading, setLoading] = useState(false)
  const [sourceNode, setSourceNode] = useState(0)
  const [targetNode, setTargetNode] = useState(33)

  useEffect(() => {
    fetch(`${API}/network`).then(r => r.json()).then(setNetwork)
    fetch(`${API}/statistics`).then(r => r.json()).then(setStats)
    fetch(`${API}/eigenvalues`).then(r => r.json()).then(setEigen)
    fetch(`${API}/matrices`).then(r => r.json()).then(setMatrices)
    fetch(`${API}/centrality`).then(r => r.json()).then(setCentrality)
  }, [])

  const runClustering = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API}/cluster`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ num_communities: k })
      })
      const data = await res.json()
      setClusterData(data)
    } catch(e) {}
    setLoading(false)
  }

  const findPath = async () => {
    try {
      const res = await fetch(`${API}/path?source=${sourceNode}&target=${targetNode}`)
      const data = await res.json()
      setPathData(data)
    } catch(e) {}
  }

  const navItems = [
    { id: '01', label: '1. Overview' },
    { id: '02', label: '2. Network Explorer' },
    { id: '03', label: '3. Node Explorer' },
    { id: '04', label: '4. Community Detection' },
    { id: '05', label: '5. Matrix Lab' },
    { id: '06', label: '6. Eigenvalues & Fiedler' },
    { id: '07', label: '7. Graph Statistics' },
    { id: '08', label: '8. Centrality Analysis' },
    { id: '09', label: '9. Shortest Path Explorer' },
    { id: '10', label: '10. Evaluation' },
    { id: '11', label: '11. Methodology & Viva' },
  ]

  const hoveredNode = hovered !== null && network ? network.nodes.find(n => n.id === hovered) : null
  const hoverComm = hoveredNode && clusterData ? clusterData.labels[hoveredNode.id] : 'N/A'

  return (
    <div className="app-container">
      {/* 3D Background Canvas */}
      <div style={{ position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 1 }}>
        <Canvas camera={{ position: [0, 0, 30], fov: 45 }}>
          <NetworkScene 
            network={network} 
            labels={clusterData ? clusterData.labels : null} 
            hovered={hovered} 
            setHovered={setHovered}
          />
        </Canvas>
      </div>

      {/* Hover Tooltip */}
      {hoveredNode && (
        <div className="hover-info" style={{ zIndex: 1000, left: 320 }}>
          <strong>Node {hoveredNode.id}</strong><br/>
          Degree: {hoveredNode.degree}<br/>
          Community: {hoverComm}
        </div>
      )}

      {/* Sidebar Navigation */}
      <div className="sidebar">
        <div className="sidebar-title">SOCIAL NETWORK LAB</div>
        {navItems.map(item => (
          <div 
            key={item.id} 
            className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            {item.label}
          </div>
        ))}
      </div>

      {/* Main Content Overlay */}
      <div className="main-content" style={{ zIndex: 10, pointerEvents: 'none', display: 'flex', alignItems: 'center', justifyContent: 'flex-end', padding: '3rem' }}>
        <div className="section-content" style={{ pointerEvents: 'auto', maxHeight: '80vh', overflowY: 'auto' }}>
          
          {activeTab === '01' && (
            <div>
              <h2>Overview</h2>
              <p>Discover hidden communities through linear algebra.</p>
              {stats && (
                <div className="stat-grid">
                  <div className="stat-box">
                    <div className="stat-val">{stats.num_nodes}</div>
                    <div className="stat-lbl">Nodes</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-val">{stats.num_edges}</div>
                    <div className="stat-lbl">Edges</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-val">{stats.avg_degree.toFixed(2)}</div>
                    <div className="stat-lbl">Avg Degree</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-val">{stats.density.toFixed(4)}</div>
                    <div className="stat-lbl">Density</div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === '02' && (
            <div>
              <h2>Network Explorer</h2>
              <p>Interact with the 3D topology directly. Rotate, pan, and zoom to explore.</p>
              <p style={{ color: 'var(--c-gold)' }}>Hover over nodes to see their immediate neighborhood highlighted.</p>
            </div>
          )}

          {activeTab === '03' && (
            <div>
              <h2>Node Explorer</h2>
              <p>Hover over the graph to inspect nodes, or use the panel below.</p>
              {hoveredNode ? (
                <div className="stat-box" style={{ borderColor: 'var(--c-turquoise)', marginTop: '1rem' }}>
                  <h3 style={{ margin: 0, color: 'var(--c-turquoise)' }}>Node {hoveredNode.id}</h3>
                  <p>Degree: {hoveredNode.degree}</p>
                  <p>Community: {hoverComm}</p>
                </div>
              ) : (
                <p>No node selected.</p>
              )}
            </div>
          )}

          {activeTab === '04' && (
            <div>
              <h2>Community Detection</h2>
              <p>Spectral clustering embeds the graph geometrically using the Laplacian's eigenvectors.</p>
              <label style={{ fontSize: '0.8rem', color: 'var(--c-mint)' }}>Number of Communities (k)</label>
              <input type="range" min="2" max="5" value={k} onChange={e => setK(parseInt(e.target.value))} style={{ width: '100%', margin: '1rem 0' }} />
              <div style={{ textAlign: 'right', fontWeight: 'bold', color: 'var(--c-gold)' }}>{k}</div>
              <button className="btn" style={{ width: '100%' }} onClick={runClustering}>
                {loading ? 'COMPUTING...' : 'RUN CLUSTERING'}
              </button>
            </div>
          )}

          {activeTab === '05' && (
            <div>
              <h2>Matrix Lab</h2>
              <p>The algebraic foundation of the graph.</p>
              {matrices ? (
                <>
                  <div className="stat-box" style={{ borderColor: 'var(--c-skyblue)', marginBottom: '1rem' }}>
                    <h3 style={{ margin: 0, color: 'var(--c-cream)' }}>Dimensions: {matrices.n} x {matrices.n}</h3>
                  </div>
                  <p><strong>A</strong> (Adjacency): Binary connections.</p>
                  <p><strong>D</strong> (Degree): Diagonal matrix of node degrees.</p>
                  <p><strong>L</strong> (Laplacian): <em>L = D - A</em></p>
                </>
              ) : <p>Loading matrices...</p>}
            </div>
          )}

          {activeTab === '06' && (
            <div>
              <h2>Eigenvalues & Fiedler</h2>
              <p>Solutions to <em>Lv = λv</em></p>
              {eigen && (
                <>
                  <div className="stat-box" style={{ borderColor: 'var(--c-gold)', marginBottom: '1rem' }}>
                    <div className="stat-val">{eigen.algebraic_connectivity.toFixed(4)}</div>
                    <div className="stat-lbl">Algebraic Connectivity (λ₂)</div>
                  </div>
                  <p style={{ fontSize: '0.85rem' }}>The Fiedler vector (v₂) signs can bi-partition the graph.</p>
                  <div style={{ height: '150px', overflowY: 'auto', background: 'rgba(0,0,0,0.3)', padding: '10px', fontSize: '0.8rem', fontFamily: 'monospace' }}>
                    {eigen.fiedler_vector.map((val, i) => (
                      <div key={i} style={{ color: val > 0 ? 'var(--c-turquoise)' : 'var(--c-coral)' }}>Node {i}: {val.toFixed(4)}</div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}

          {activeTab === '07' && (
            <div>
              <h2>Graph Statistics</h2>
              {stats && (
                <div className="stat-grid">
                  <div className="stat-box">
                    <div className="stat-val">{stats.clustering_coefficient.toFixed(3)}</div>
                    <div className="stat-lbl">Avg Clustering Coeff</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-val">{stats.avg_shortest_path ? stats.avg_shortest_path.toFixed(3) : 'N/A'}</div>
                    <div className="stat-lbl">Avg Path Length</div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === '08' && (
            <div>
              <h2>Centrality Analysis</h2>
              <p>Which nodes are the most important?</p>
              {centrality && (
                <div style={{ height: '200px', overflowY: 'auto', background: 'rgba(0,0,0,0.3)', padding: '10px', fontSize: '0.85rem' }}>
                  {Object.entries(centrality.degree)
                    .sort((a,b) => b[1] - a[1])
                    .slice(0, 10)
                    .map(([n, val], i) => (
                      <div key={n} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                        <span>Rank {i+1}: Node {n}</span>
                        <strong style={{ color: 'var(--c-turquoise)' }}>{val.toFixed(4)}</strong>
                      </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === '09' && (
            <div>
              <h2>Shortest Path Explorer</h2>
              <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
                <input type="number" value={sourceNode} onChange={e => setSourceNode(e.target.value)} style={{ width: '60px' }} />
                <span style={{ color: 'var(--c-mint)' }}>to</span>
                <input type="number" value={targetNode} onChange={e => setTargetNode(e.target.value)} style={{ width: '60px' }} />
              </div>
              <button className="btn" onClick={findPath}>FIND PATH</button>
              
              {pathData && (
                <div className="stat-box" style={{ marginTop: '1rem' }}>
                  {pathData.length > 0 ? (
                    <>
                      <p>Path Length: <strong>{pathData.length}</strong></p>
                      <p style={{ wordBreak: 'break-all', color: 'var(--c-turquoise)' }}>{pathData.path.join(' → ')}</p>
                    </>
                  ) : <p style={{ color: 'var(--c-coral)' }}>No path exists.</p>}
                </div>
              )}
            </div>
          )}

          {activeTab === '10' && (
            <div>
              <h2>Evaluation</h2>
              {clusterData ? (
                <>
                  <div className="stat-box" style={{ marginBottom: '1rem', borderColor: 'var(--c-turquoise)' }}>
                    <div className="stat-val">{clusterData.modularity.toFixed(4)}</div>
                    <div className="stat-lbl">Modularity</div>
                  </div>
                  {clusterData.ari !== null && (
                    <div className="stat-box" style={{ borderColor: 'var(--c-gold)' }}>
                      <div className="stat-val">{clusterData.ari.toFixed(4)}</div>
                      <div className="stat-lbl">Adjusted Rand Index</div>
                    </div>
                  )}
                </>
              ) : <p>Run Community Detection first.</p>}
            </div>
          )}
          
          {activeTab === '11' && (
            <div>
              <h2>Methodology & Viva</h2>
              <h3 style={{ color: 'var(--c-mint)' }}>Q: Why use the Graph Laplacian?</h3>
              <p style={{ fontSize: '0.85rem' }}>The Laplacian <em>L = D - A</em> acts like a differential operator on the graph. Minimizing the quadratic form <em>x^T L x</em> finds a node assignment that cuts the fewest edges.</p>
              
              <h3 style={{ color: 'var(--c-mint)' }}>Q: What is the Fiedler Vector?</h3>
              <p style={{ fontSize: '0.85rem' }}>It is the eigenvector corresponding to the second smallest eigenvalue (λ₂) of L. Its values provide a 1D geometrical embedding of the network.</p>
            </div>
          )}

        </div>
      </div>
    </div>
  )
}
