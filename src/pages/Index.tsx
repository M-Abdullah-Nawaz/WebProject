
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Index = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Welcome to User Settings Demo</h1>
        <p className="text-xl text-gray-600 mb-8">Click below to access the settings page</p>
        <Link to="/settings">
          <Button className="bg-red-600 hover:bg-red-700">Go to Settings</Button>
        </Link>
      </div>
    </div>
  );
};

export default Index;
