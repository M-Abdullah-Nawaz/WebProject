
import React, { useState } from 'react';
import { Minus, Plus } from 'lucide-react';

interface SettingsSectionProps {
  title: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}

const SettingsSection = ({ title, defaultOpen = false, children }: SettingsSectionProps) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="mb-8 border-l-2 border-red-600">
      <div className="flex items-center justify-between pl-4">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        <button 
          onClick={() => setIsOpen(!isOpen)} 
          className="p-1 rounded-md hover:bg-gray-100"
          aria-label={isOpen ? "Collapse section" : "Expand section"}
        >
          {isOpen ? <Minus size={18} /> : <Plus size={18} />}
        </button>
      </div>
      
      {isOpen && (
        <div className="mt-4 pl-4">
          {children}
        </div>
      )}
    </div>
  );
};

export default SettingsSection;
