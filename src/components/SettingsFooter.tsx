
import React from 'react';
import { Button } from '@/components/ui/button';

const SettingsFooter = () => {
  return (
    <div className="flex justify-end mt-12 mb-8">
      <Button variant="destructive">Logout</Button>
    </div>
  );
};

export default SettingsFooter;
