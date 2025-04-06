
import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const ChangePasswordSection = () => {
  return (
    <div className="space-y-6 max-w-md">
      <div>
        <label htmlFor="new-password" className="block text-sm font-medium text-gray-700 mb-1">
          New Password
        </label>
        <Input
          id="new-password"
          type="password"
          placeholder="Enter new password"
          className="w-full"
        />
      </div>

      <div>
        <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-700 mb-1">
          Confirm Password
        </label>
        <Input
          id="confirm-password"
          type="password"
          placeholder="Confirm new password"
          className="w-full"
        />
      </div>

      <Button variant="destructive" className="px-4">
        Save New Password
      </Button>
    </div>
  );
};

export default ChangePasswordSection;
