import React from 'react';

interface AIRecommendationsProps {
  materials: Array<{
    id: string;
    name: string;
    cost: number;
    sustainabilityScore: number;
  }>;
  onSelect: (materialId: string) => void;
}

export const AIRecommendations: React.FC<AIRecommendationsProps> = ({ materials, onSelect }) => {
  return (
    <div className="ai-recommendations">
      <h3>AI Recommendations</h3>
      <ul>
        {materials.map((material) => (
          <li key={material.id} onClick={() => onSelect(material.id)}>
            {material.name} - ${material.cost} (Score: {material.sustainabilityScore})
          </li>
        ))}
      </ul>
    </div>
  );
};
