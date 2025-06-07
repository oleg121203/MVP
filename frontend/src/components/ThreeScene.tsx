import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import { Suspense } from 'react';
import BuildingModel from './BuildingModel';

export default function ThreeScene() {
  return (
    <Canvas>
      <Suspense fallback={null}>
        <Environment preset="city" />
        <OrbitControls makeDefault />
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <BuildingModel />
      </Suspense>
    </Canvas>
  );
}
