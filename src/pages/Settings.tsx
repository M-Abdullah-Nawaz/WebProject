
import React from 'react';
import SettingsHeader from '@/components/SettingsHeader';
import SettingsSection from '@/components/SettingsSection';
import ProfileSection from '@/components/ProfileSection';
import LanguageSection from '@/components/LanguageSection';
import SubscriptionPlanSection from '@/components/SubscriptionPlanSection';
import UpdateGenresSection from '@/components/UpdateGenresSection';
import ChangePasswordSection from '@/components/ChangePasswordSection';
import SettingsFooter from '@/components/SettingsFooter';

const Settings = () => {
  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <SettingsHeader />
      
      <div className="space-y-6">
        <SettingsSection title="Profile" defaultOpen={true}>
          <ProfileSection />
        </SettingsSection>
        
        <SettingsSection title="languageChoose">
          <LanguageSection />
        </SettingsSection>
        
        <SettingsSection title="Subscription Plan">
          <SubscriptionPlanSection />
        </SettingsSection>
        
        <SettingsSection title="Update Genres">
          <UpdateGenresSection />
        </SettingsSection>
        
        <SettingsSection title="Change Password">
          <ChangePasswordSection />
        </SettingsSection>
      </div>
      
      <SettingsFooter />
    </div>
  );
};

export default Settings;
