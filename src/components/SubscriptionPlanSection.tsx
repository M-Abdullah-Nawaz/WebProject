
import React from 'react';
import { Button } from '@/components/ui/button';
import { Check } from 'lucide-react';

const SubscriptionPlanSection = () => {
  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
        {/* Free Plan */}
        <div className="border border-gray-200 rounded-lg p-6 flex flex-col">
          <h4 className="font-semibold text-lg">Free Plan</h4>
          <p className="text-sm text-gray-500 mt-1 mb-4">Lorem ipsum dolor sit amet consectetur</p>
          <div className="text-xs text-gray-600 mb-4">
            <p>Lorem ipsum dolor sit amet consectetur.</p>
            <p>Voluptate, voluptas, at si dolores sunt.</p>
            <p>Labore fugiat.</p>
          </div>
          <div className="mt-auto">
            <p className="text-2xl font-bold mb-2">$0</p>
            <Button variant="outline" className="w-full bg-lime-400 hover:bg-lime-500 border-lime-500 text-white">Choose Plan</Button>
          </div>
          <div className="mt-4">
            <p className="font-medium text-sm mb-2">Featured Services</p>
            <div className="space-y-1">
              <div className="flex items-center text-xs">
                <div className="w-4 h-4 rounded-full border border-gray-300 mr-2"></div>
                <span>20 free uploads</span>
              </div>
              <div className="flex items-center text-xs">
                <div className="w-4 h-4 rounded-full border border-gray-300 mr-2"></div>
                <span>Ad break</span>
              </div>
            </div>
          </div>
        </div>

        {/* Basic Plan */}
        <div className="border border-gray-200 rounded-lg p-6 flex flex-col">
          <h4 className="font-semibold text-lg">Basic Plan</h4>
          <p className="text-sm text-gray-500 mt-1 mb-4">Lorem ipsum dolor sit amet consectetur</p>
          <div className="text-xs text-gray-600 mb-4">
            <p>Lorem ipsum dolor sit amet consectetur.</p>
            <p>Voluptate, voluptas, at si dolores sunt.</p>
            <p>Labore fugiat.</p>
          </div>
          <div className="mt-auto">
            <p className="text-2xl font-bold mb-2">$25</p>
            <Button variant="outline" className="w-full bg-blue-400 hover:bg-blue-500 border-blue-500 text-white">Choose Plan</Button>
          </div>
          <div className="mt-4">
            <p className="font-medium text-sm mb-2">Featured Services</p>
            <div className="space-y-1">
              <div className="flex items-center text-xs">
                <div className="w-4 h-4 rounded-full bg-blue-500 text-white flex items-center justify-center mr-2">
                  <Check size={12} />
                </div>
                <span>Ad-free experience</span>
              </div>
              <div className="flex items-center text-xs">
                <div className="w-4 h-4 rounded-full border border-gray-300 mr-2"></div>
                <span>Ad break</span>
              </div>
            </div>
          </div>
        </div>

        {/* Standard Plan */}
        <div className="border border-gray-200 rounded-lg p-6 flex flex-col">
          <h4 className="font-semibold text-lg">Standard Plan</h4>
          <p className="text-sm text-gray-500 mt-1 mb-4">Lorem ipsum dolor sit amet consectetur</p>
          <div className="text-xs text-gray-600 mb-4">
            <p>Lorem ipsum dolor sit amet consectetur.</p>
            <p>Voluptate, voluptas, at si dolores sunt.</p>
            <p>Labore fugiat.</p>
          </div>
          <div className="mt-auto">
            <p className="text-2xl font-bold mb-2">$35</p>
            <Button variant="outline" className="w-full bg-orange-400 hover:bg-orange-500 border-orange-500 text-white">Choose Plan</Button>
          </div>
          <div className="mt-4">
            <p className="font-medium text-sm mb-2">Featured Services</p>
            <div className="space-y-1">
              <div className="flex items-center text-xs">
                <div className="w-4 h-4 rounded-full bg-orange-500 text-white flex items-center justify-center mr-2">
                  <Check size={12} />
                </div>
                <span>Ad-free experience</span>
              </div>
              <div className="flex items-center text-xs">
                <div className="w-4 h-4 rounded-full bg-orange-500 text-white flex items-center justify-center mr-2">
                  <Check size={12} />
                </div>
                <span>24/7 support</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-center mt-6">
        <Button variant="outline" className="text-blue-500 border-none rounded-full">
          More
        </Button>
      </div>
    </div>
  );
};

export default SubscriptionPlanSection;
