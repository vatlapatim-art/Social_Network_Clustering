import React, { useRef, useMemo } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls, Stars, Line } from '@react-three/drei'
import * as THREE from 'three'

const COLORS = {
  turquoise: '#40DCC0',
  coral: '#FF8066',
  skyBlue: '#58B7FF',
  gold: '#F4C95D',
  mint: '#8BE0A5',
  default: '#40DCC0',
  connection: '#8BBFC4',
  dimConnection: '#1B4148',
  dimNode: '#173941'
}
const COMM_COLORS = [COLORS.turquoise, COLORS.coral, COLORS.gold, COLORS.skyBlue, COLORS.mint]

const NodeMesh = ({ node, labels, hovered, setHovered, neighbors }) => {
  const comm = labels ? labels[node.id] : null
  let baseColor = comm !== null && comm !== undefined ? COMM_COLORS[comm % COMM_COLORS.length] : COLORS.default
  
  const isHovered = hovered === node.id
  const isNeighbor = hovered !== null && neighbors.includes(node.id)
  const isDimmed = hovered !== null && !isHovered && !isNeighbor
  
  const color = isDimmed ? COLORS.dimNode : baseColor
  const opacity = isDimmed ? 0.3 : 1.0

  return (
    <mesh 
      position={[node.x * 12, node.y * 12, node.z * 12]}
      onPointerOver={(e) => { e.stopPropagation(); setHovered(node.id) }}
      onPointerOut={() => setHovered(null)}
    >
      <sphereGeometry args={[isHovered ? 0.4 : 0.25, 32, 32]} />
      <meshStandardMaterial 
        color={color} 
        emissive={color} 
        emissiveIntensity={isHovered ? 0.8 : (isDimmed ? 0.0 : 0.4)} 
        roughness={0.2} 
        transparent
        opacity={opacity}
      />
    </mesh>
  )
}

const Edges = ({ nodes, edges, hovered, getNeighbors }) => {
  const lines = useMemo(() => {
    return edges.map(e => {
      const source = nodes.find(n => n.id === e.source)
      const target = nodes.find(n => n.id === e.target)
      if (!source || !target) return null
      
      const isHoveredEdge = hovered !== null && (e.source === hovered || e.target === hovered)
      const isDimmedEdge = hovered !== null && !isHoveredEdge
      
      const color = isDimmedEdge ? COLORS.dimConnection : COLORS.connection
      const lineWidth = isHoveredEdge ? 2.5 : 1.0
      const opacity = isDimmedEdge ? 0.1 : 0.8
      
      return {
        points: [
          new THREE.Vector3(source.x * 12, source.y * 12, source.z * 12),
          new THREE.Vector3(target.x * 12, target.y * 12, target.z * 12)
        ],
        color, lineWidth, opacity
      }
    }).filter(Boolean)
  }, [nodes, edges, hovered])

  return (
    <group>
      {lines.map((line, i) => (
        <Line 
          key={i} 
          points={line.points} 
          color={line.color} 
          lineWidth={line.lineWidth} 
          transparent 
          opacity={line.opacity} 
          depthTest={true}
        />
      ))}
    </group>
  )
}

export default function NetworkScene({ network, labels, hovered, setHovered }) {
  const groupRef = useRef()

  useFrame((state) => {
    if (groupRef.current && hovered === null) {
      groupRef.current.rotation.y += 0.0005
    }
  })

  if (!network || !network.nodes) return null

  const getNeighbors = (nodeId) => {
    if (nodeId === null) return []
    return network.edges.reduce((acc, edge) => {
      if (edge.source === nodeId) acc.push(edge.target)
      if (edge.target === nodeId) acc.push(edge.source)
      return acc
    }, [])
  }
  
  const neighbors = getNeighbors(hovered)

  return (
    <>
      <ambientLight intensity={0.6} />
      <directionalLight position={[10, 10, 5]} intensity={1} color={COLORS.mint} />
      <pointLight position={[-10, -10, -10]} intensity={0.5} color={COLORS.skyBlue} />
      
      <Stars radius={100} depth={50} count={1000} factor={3} saturation={0} fade speed={1} />
      <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} makeDefault />

      <group ref={groupRef}>
        <Edges nodes={network.nodes} edges={network.edges} hovered={hovered} />
        {network.nodes.map(n => (
          <NodeMesh 
            key={n.id} 
            node={n} 
            labels={labels} 
            hovered={hovered} 
            setHovered={setHovered}
            neighbors={neighbors}
          />
        ))}
      </group>
    </>
  )
}
