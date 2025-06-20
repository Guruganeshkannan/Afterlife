import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    UserIcon,
    EnvelopeIcon,
    LockClosedIcon,
    DocumentTextIcon,
    MicrophoneIcon,
    PhotoIcon,
} from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../config';

interface UserProfile {
    id: number;
    email: string;
    full_name: string;
    personality_data: string;
    writing_samples: string;
    voice_samples: string;
}

const Profile = () => {
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState<Partial<UserProfile>>({});
    const [passwordData, setPasswordData] = useState({
        current_password: '',
        new_password: '',
        confirm_password: '',
    });
    const [passwordError, setPasswordError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchProfile();
    }, [navigate]);

    const fetchProfile = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            const response = await fetch(`${API_URL}/users/me`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch profile');
            }

            const data = await response.json();
            setProfile(data);
            setFormData(data);
        } catch (error) {
            console.error('Error fetching profile:', error);
            setError('Failed to load profile. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateProfile = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            const response = await fetch(`${API_URL}/users/me`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(profile),
            });

            if (!response.ok) {
                throw new Error('Failed to update profile');
            }

            const updatedProfile = await response.json();
            setProfile(updatedProfile);
            setSuccess('Profile updated successfully');
        } catch (error) {
            console.error('Error updating profile:', error);
            setError('Failed to update profile. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleUpdatePassword = async (e: React.FormEvent) => {
        e.preventDefault();
        setPasswordError('');

        if (passwordData.new_password !== passwordData.confirm_password) {
            setPasswordError('New passwords do not match');
            return;
        }

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('No authentication token');
            }

            const response = await fetch('http://localhost:8001/api/v1/users/me/password', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    current_password: passwordData.current_password,
                    new_password: passwordData.new_password,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to update password');
            }

            setPasswordData({
                current_password: '',
                new_password: '',
                confirm_password: '',
            });
        } catch (err) {
            setPasswordError('Failed to update password. Please try again.');
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    if (!profile) {
        return (
            <div className="text-center py-12">
                <h2 className="text-2xl font-semibold text-gray-900">Profile not found</h2>
                <p className="mt-2 text-gray-600">Unable to load your profile information.</p>
            </div>
        );
    }

    return (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-8"
            >
                {/* Profile Information */}
                <div className="bg-white shadow sm:rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-lg font-medium leading-6 text-gray-900">Profile Information</h2>
                            <button
                                onClick={() => setIsEditing(!isEditing)}
                                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                            >
                                {isEditing ? 'Cancel' : 'Edit Profile'}
                            </button>
                        </div>

                        {error && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="mb-4 rounded-md bg-red-50 p-4"
                            >
                                <div className="text-sm text-red-700">{error}</div>
                            </motion.div>
                        )}

                        {isEditing ? (
                            <motion.form
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                onSubmit={handleUpdateProfile}
                                className="space-y-6"
                            >
                                <div>
                                    <label htmlFor="full_name" className="block text-sm font-medium text-gray-700">
                                        Full Name
                                    </label>
                                    <div className="mt-1 relative rounded-md shadow-sm">
                                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                            <UserIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                        </div>
                                        <input
                                            type="text"
                                            name="full_name"
                                            id="full_name"
                                            required
                                            className="input-field pl-10"
                                            value={formData.full_name}
                                            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                                        Email
                                    </label>
                                    <div className="mt-1 relative rounded-md shadow-sm">
                                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                            <EnvelopeIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                        </div>
                                        <input
                                            type="email"
                                            name="email"
                                            id="email"
                                            required
                                            className="input-field pl-10"
                                            value={formData.email}
                                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label htmlFor="personality_data" className="block text-sm font-medium text-gray-700">
                                        Personality Data
                                    </label>
                                    <div className="mt-1 relative rounded-md shadow-sm">
                                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                            <DocumentTextIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                        </div>
                                        <textarea
                                            id="personality_data"
                                            name="personality_data"
                                            rows={4}
                                            className="input-field pl-10"
                                            value={formData.personality_data}
                                            onChange={(e) => setFormData({ ...formData, personality_data: e.target.value })}
                                        />
                                    </div>
                                </div>

                                <div className="flex justify-end">
                                    <button
                                        type="submit"
                                        className="btn-primary"
                                    >
                                        Save Changes
                                    </button>
                                </div>
                            </motion.form>
                        ) : (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="space-y-6"
                            >
                                <div>
                                    <dt className="text-sm font-medium text-gray-500">Full Name</dt>
                                    <dd className="mt-1 text-sm text-gray-900">{profile.full_name}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm font-medium text-gray-500">Email</dt>
                                    <dd className="mt-1 text-sm text-gray-900">{profile.email}</dd>
                                </div>
                                <div>
                                    <dt className="text-sm font-medium text-gray-500">Personality Data</dt>
                                    <dd className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">
                                        {profile.personality_data || 'No personality data provided'}
                                    </dd>
                                </div>
                            </motion.div>
                        )}
                    </div>
                </div>

                {/* Change Password */}
                <div className="bg-white shadow sm:rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <h2 className="text-lg font-medium leading-6 text-gray-900">Change Password</h2>
                        <div className="mt-5">
                            <motion.form
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                onSubmit={handleUpdatePassword}
                                className="space-y-6"
                            >
                                {passwordError && (
                                    <motion.div
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        className="rounded-md bg-red-50 p-4"
                                    >
                                        <div className="text-sm text-red-700">{passwordError}</div>
                                    </motion.div>
                                )}

                                <div>
                                    <label htmlFor="current_password" className="block text-sm font-medium text-gray-700">
                                        Current Password
                                    </label>
                                    <div className="mt-1 relative rounded-md shadow-sm">
                                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                            <LockClosedIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                        </div>
                                        <input
                                            type="password"
                                            name="current_password"
                                            id="current_password"
                                            required
                                            className="input-field pl-10"
                                            value={passwordData.current_password}
                                            onChange={(e) =>
                                                setPasswordData({ ...passwordData, current_password: e.target.value })
                                            }
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label htmlFor="new_password" className="block text-sm font-medium text-gray-700">
                                        New Password
                                    </label>
                                    <div className="mt-1 relative rounded-md shadow-sm">
                                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                            <LockClosedIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                        </div>
                                        <input
                                            type="password"
                                            name="new_password"
                                            id="new_password"
                                            required
                                            className="input-field pl-10"
                                            value={passwordData.new_password}
                                            onChange={(e) =>
                                                setPasswordData({ ...passwordData, new_password: e.target.value })
                                            }
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700">
                                        Confirm New Password
                                    </label>
                                    <div className="mt-1 relative rounded-md shadow-sm">
                                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                            <LockClosedIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                        </div>
                                        <input
                                            type="password"
                                            name="confirm_password"
                                            id="confirm_password"
                                            required
                                            className="input-field pl-10"
                                            value={passwordData.confirm_password}
                                            onChange={(e) =>
                                                setPasswordData({ ...passwordData, confirm_password: e.target.value })
                                            }
                                        />
                                    </div>
                                </div>

                                <div className="flex justify-end">
                                    <button
                                        type="submit"
                                        className="btn-primary"
                                    >
                                        Update Password
                                    </button>
                                </div>
                            </motion.form>
                        </div>
                    </div>
                </div>

                {/* Media Samples */}
                <div className="bg-white shadow sm:rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <h2 className="text-lg font-medium leading-6 text-gray-900">Media Samples</h2>
                        <div className="mt-5 space-y-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Writing Samples</label>
                                <div className="mt-1">
                                    <textarea
                                        rows={4}
                                        className="input-field"
                                        value={profile.writing_samples || ''}
                                        readOnly
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700">Voice Samples</label>
                                <div className="mt-1">
                                    <div className="flex items-center space-x-4">
                                        <MicrophoneIcon className="h-5 w-5 text-gray-400" />
                                        <span className="text-sm text-gray-500">
                                            {profile.voice_samples ? 'Voice samples uploaded' : 'No voice samples uploaded'}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700">Photos</label>
                                <div className="mt-1">
                                    <div className="flex items-center space-x-4">
                                        <PhotoIcon className="h-5 w-5 text-gray-400" />
                                        <span className="text-sm text-gray-500">
                                            {profile.voice_samples ? 'Photos uploaded' : 'No photos uploaded'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default Profile; 