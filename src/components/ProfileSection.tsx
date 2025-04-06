
import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const ProfileSection = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <div className="relative">
          <img 
            src="/lovable-uploads/352cfe6f-3ceb-4c8e-b7eb-0fc09c6454f5.png" 
            alt="Profile" 
            className="w-16 h-16 rounded-full object-cover"
          />
        </div>
        <div>
          <p className="text-sm text-gray-600">Please use an image less than 10MB</p>
          <div className="flex gap-3 mt-2">
            <Button variant="destructive" size="sm" className="text-xs py-1 px-4">Upload New</Button>
            <Button variant="outline" size="sm" className="text-xs py-1 px-4 border-gray-300 text-gray-700">Delete Avatar</Button>
          </div>
        </div>
      </div>

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">Name</label>
        <Input id="name" type="text" placeholder="Full Name" className="w-full max-w-md" />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <Input id="email" type="email" placeholder="your.email@example.com" className="w-full max-w-md" />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">Password</label>
        <Input id="password" type="password" placeholder="********" className="w-full max-w-md" />
      </div>

      <Button variant="destructive" className="mt-4 px-4">Save Changes</Button>
    </div>
  );
};

export default ProfileSection;
