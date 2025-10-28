'use client';

import { useState } from 'react';
import RecentUsersCarousel from './RecentUsersCarousel';

interface User {
  id: number;
  username: string;
  age: number;
  eyeColor: string;
}

const mockData: User[] = [
  { id: 1, username: 'alice_smith', age: 28, eyeColor: 'Brown' },
  { id: 2, username: 'bob_johnson', age: 34, eyeColor: 'Blue' },
  { id: 3, username: 'charlie_brown', age: 22, eyeColor: 'Green' },
  { id: 4, username: 'diana_prince', age: 29, eyeColor: 'Hazel' },
  { id: 5, username: 'eve_adams', age: 31, eyeColor: 'Brown' },
];

export default function UserTable() {
  const [users, setUsers] = useState<User[]>(mockData);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [formData, setFormData] = useState({ username: '', age: '', eyeColor: 'Brown' });

  const handleDelete = (id: number) => {
    setUsers(users.filter(user => user.id !== id));
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    setFormData({
      username: user.username,
      age: user.age.toString(),
      eyeColor: user.eyeColor
    });
    setIsModalOpen(true);
  };

  const handleAdd = () => {
    setEditingUser(null);
    setFormData({ username: '', age: '', eyeColor: 'Brown' });
    setIsModalOpen(true);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.username || !formData.age) {
      alert('Please fill in all fields');
      return;
    }

    const age = parseInt(formData.age);
    if (isNaN(age) || age <= 0) {
      alert('Please enter a valid age');
      return;
    }

    if (editingUser) {
      // Update existing user
      setUsers(users.map(user => 
        user.id === editingUser.id 
          ? { ...user, username: formData.username, age, eyeColor: formData.eyeColor }
          : user
      ));
    } else {
      // Add new user
      const newId = Math.max(...users.map(u => u.id), 0) + 1;
      setUsers([...users, { id: newId, username: formData.username, age, eyeColor: formData.eyeColor }]);
    }

    setIsModalOpen(false);
    setFormData({ username: '', age: '', eyeColor: 'Brown' });
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setFormData({ username: '', age: '', eyeColor: 'Brown' });
  };

  return (
    <>
      <div className="w-full max-w-4xl mx-auto p-6 font-inter">
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20">
          <div className="p-8">
            <h2 className="text-3xl font-semibold text-gray-800 mb-8 tracking-tight">User Management</h2>
            
            <div className="overflow-x-auto rounded-lg border border-gray-100">
              <table className="w-full">
                <thead>
                  <tr className="bg-gradient-to-r from-indigo-50 to-purple-50 border-b border-gray-200">
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Username
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Age
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Eye Color
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-100">
                  {users.map((user) => (
                    <tr key={user.id} className="hover:bg-gradient-to-r hover:from-indigo-50/30 hover:to-purple-50/30 transition-all duration-200">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {user.username}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-700">
                          {user.age}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <div 
                            className="w-4 h-4 rounded-full border-2 border-gray-200 shadow-sm"
                            style={{ backgroundColor: user.eyeColor.toLowerCase() }}
                          ></div>
                          <span className="text-sm text-gray-700">{user.eyeColor}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-3">
                          <button 
                            onClick={() => handleEdit(user)}
                            className="px-4 py-1.5 bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white text-sm font-medium rounded-lg shadow-sm hover:shadow-md transition-all duration-200 transform hover:scale-105 active:scale-95"
                          >
                            Edit
                          </button>
                          <button 
                            onClick={() => handleDelete(user.id)}
                            className="px-4 py-1.5 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white text-sm font-medium rounded-lg shadow-sm hover:shadow-md transition-all duration-200 transform hover:scale-105 active:scale-95"
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-8 flex justify-between items-center">
              <div className="text-sm text-gray-500">
                Showing <span className="font-semibold text-gray-700">{users.length}</span> users
              </div>
              <button 
                onClick={handleAdd}
                className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 active:scale-95"
              >
                + Add New User
              </button>
            </div>
          </div>
        </div>

        {/* Recent Users Carousel */}
        <RecentUsersCarousel users={users} />
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 transform transition-all">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-semibold text-gray-800">
                {editingUser ? 'Edit User' : 'Add New User'}
              </h3>
              <button
                onClick={handleCloseModal}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Username
                </label>
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-gray-900 placeholder:text-gray-400"
                  placeholder="Enter username"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Age
                </label>
                <input
                  type="number"
                  value={formData.age}
                  onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-gray-900 placeholder:text-gray-400"
                  placeholder="Enter age"
                  min="1"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Eye Color
                </label>
                <select
                  value={formData.eyeColor}
                  onChange={(e) => setFormData({ ...formData, eyeColor: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-gray-900"
                >
                  <option value="Brown">Brown</option>
                  <option value="Blue">Blue</option>
                  <option value="Green">Green</option>
                  <option value="Hazel">Hazel</option>
                  <option value="Gray">Gray</option>
                  <option value="Amber">Amber</option>
                </select>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-all font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white rounded-lg shadow-sm hover:shadow-md transition-all font-medium"
                >
                  {editingUser ? 'Update' : 'Add'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}