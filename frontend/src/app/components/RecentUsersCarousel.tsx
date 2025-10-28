'use client';

import { useState, useEffect } from 'react';

interface User {
  id: number;
  username: string;
  age: number;
  eyeColor: string;
}

interface RecentUsersCarouselProps {
  users: User[];
}

export default function RecentUsersCarousel({ users }: RecentUsersCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  // Get the 3 most recent users (last 3 added)
  const recentUsers = users.slice(-3);
  
  // If we have less than 3 users, don't show carousel
  if (recentUsers.length === 0) {
    return null;
  }

  useEffect(() => {
    if (recentUsers.length <= 1) return;

    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % recentUsers.length);
    }, 3000);

    return () => clearInterval(interval);
  }, [recentUsers.length]);

  const currentUser = recentUsers[currentIndex];

  return (
    <div className="w-full max-w-4xl mx-auto px-6 mt-8 mb-6">
      <div className="bg-gradient-to-br from-white/90 to-indigo-50/40 backdrop-blur-sm rounded-2xl shadow-2xl border-2 border-indigo-200/50 p-8">
        <h3 className="text-xl font-semibold text-gray-700 mb-4 text-center">
          👥 Recently Added
        </h3>
        
        <div className="relative overflow-hidden" style={{ minHeight: '120px' }}>
          <div
            key={currentUser.id}
            className="animate-fadeIn"
            style={{
              animation: 'fadeIn 0.5s ease-in'
            }}
          >
            <div className="bg-white/70 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-indigo-100">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-6">
                  <div className="relative">
                    <div 
                      className="w-16 h-16 rounded-full border-3 border-indigo-200 shadow-md"
                      style={{ backgroundColor: currentUser.eyeColor.toLowerCase() }}
                    ></div>
                    <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-indigo-500 rounded-full border-2 border-white"></div>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Name</p>
                    <p className="text-2xl font-semibold text-gray-800">{currentUser.username}</p>
                  </div>
                </div>

                <div className="flex items-center gap-8">
                  <div>
                    <p className="text-sm text-gray-500 mb-1">Eye Color</p>
                    <div className="flex items-center gap-2">
                      <div 
                        className="w-4 h-4 rounded-full border-2 border-gray-200"
                        style={{ backgroundColor: currentUser.eyeColor.toLowerCase() }}
                      ></div>
                      <p className="text-lg font-medium text-gray-800">{currentUser.eyeColor}</p>
                    </div>
                  </div>

                  <div className="h-12 w-px bg-gradient-to-b from-indigo-200 to-indigo-100"></div>

                  <div>
                    <p className="text-sm text-gray-500 mb-1">Age</p>
                    <p className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                      {currentUser.age}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Dots indicator */}
        <div className="flex justify-center gap-2 mt-6">
          {recentUsers.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={`transition-all duration-300 ${
                index === currentIndex
                  ? 'w-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full'
                  : 'w-2 h-2 bg-indigo-300 rounded-full hover:bg-indigo-400'
              }`}
              style={{ height: '8px' }}
              aria-label={`Go to user ${index + 1}`}
            />
          ))}
        </div>

        <div className="text-center mt-4">
          <p className="text-xs text-gray-400">
            {currentIndex + 1} of {recentUsers.length}
          </p>
        </div>
      </div>
    </div>
  );
}

