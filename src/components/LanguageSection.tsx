
import React from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const LanguageSection = () => {
  return (
    <div className="max-w-md">
      <label htmlFor="language-select" className="block text-sm font-medium text-gray-700 mb-1">Select a language</label>
      <Select defaultValue="english">
        <SelectTrigger className="w-full" id="language-select">
          <SelectValue placeholder="Select language" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="english">English</SelectItem>
          <SelectItem value="spanish">Spanish</SelectItem>
          <SelectItem value="french">French</SelectItem>
          <SelectItem value="german">German</SelectItem>
          <SelectItem value="chinese">Chinese</SelectItem>
          <SelectItem value="japanese">Japanese</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
};

export default LanguageSection;
