import UserTable from './components/UserTable';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Animated background */}
      <div className="animated-gradient"></div>
      <div className="pastel-vignette"></div>
      
      {/* Floating blobs */}
      <div className="blob w-96 h-96 bg-blue-300 top-10 left-10" style={{ animationDelay: '0s' }}></div>
      <div className="blob w-80 h-80 bg-pink-300 top-20 right-20" style={{ animationDelay: '4s' }}></div>
      <div className="blob w-72 h-72 bg-green-300 bottom-20 left-20" style={{ animationDelay: '8s' }}></div>
      
      {/* Main content */}
      <div className="relative z-10">
        <UserTable />
      </div>
    </div>
  );
}
