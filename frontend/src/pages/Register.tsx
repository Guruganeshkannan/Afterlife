import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    EnvelopeIcon,
    LockClosedIcon,
    UserIcon,
    DocumentTextIcon,
} from '@heroicons/react/24/outline';
import { API_URL } from '../config';

const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        full_name: '',
        personality_data: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            // Prepare the request body according to the backend schema
            const requestBody = {
                email: formData.email,
                password: formData.password,
                full_name: formData.full_name,
                personality_data: formData.personality_data ? JSON.parse(formData.personality_data) : null,
            };

            const response = await fetch(`${API_URL}/users/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Registration failed');
            }

            // After successful registration, log the user in
            const loginResponse = await fetch(`${API_URL}/login/access-token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username: formData.email,
                    password: formData.password,
                }),
            });

            if (!loginResponse.ok) {
                throw new Error('Registration successful but login failed');
            }

            const loginData = await loginResponse.json();
            localStorage.setItem('token', loginData.access_token);
            navigate('/dashboard');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Registration failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="text-center"
                >
                    <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
                        Create your{' '}
                        <span className="text-primary-600">AfterLife</span>{' '}
                        account
                    </h2>
                    <p className="mt-2 text-sm text-gray-600">
                        Or{' '}
                        <Link
                            to="/login"
                            className="font-medium text-primary-600 hover:text-primary-500"
                        >
                            sign in to your account
                        </Link>
                    </p>
                </motion.div>

                <motion.form
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                    className="mt-8 space-y-6"
                    onSubmit={handleSubmit}
                >
                    <div className="rounded-md shadow-sm -space-y-px">
                        <div className="relative">
                            <label htmlFor="full_name" className="sr-only">
                                Full Name
                            </label>
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <UserIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </div>
                            <input
                                id="full_name"
                                name="full_name"
                                type="text"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 pl-10 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                                placeholder="Full Name"
                                value={formData.full_name}
                                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                            />
                        </div>
                        <div className="relative">
                            <label htmlFor="email" className="sr-only">
                                Email address
                            </label>
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <EnvelopeIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </div>
                            <input
                                id="email"
                                name="email"
                                type="email"
                                autoComplete="email"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 pl-10 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                                placeholder="Email address"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            />
                        </div>
                        <div className="relative">
                            <label htmlFor="password" className="sr-only">
                                Password
                            </label>
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <LockClosedIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </div>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                autoComplete="new-password"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-2 pl-10 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                                placeholder="Password"
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            />
                        </div>
                        <div className="relative">
                            <label htmlFor="personality_data" className="sr-only">
                                Personality Data
                            </label>
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <DocumentTextIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </div>
                            <textarea
                                id="personality_data"
                                name="personality_data"
                                rows={3}
                                className="appearance-none rounded-none relative block w-full px-3 py-2 pl-10 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
                                placeholder="Tell us about yourself (optional)"
                                value={formData.personality_data}
                                onChange={(e) => setFormData({ ...formData, personality_data: e.target.value })}
                            />
                        </div>
                    </div>

                    {error && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-red-500 text-sm text-center"
                        >
                            {error}
                        </motion.div>
                    )}

                    <div>
                        <button
                            type="submit"
                            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                        >
                            Create account
                        </button>
                    </div>
                </motion.form>
            </div>
        </div>
    );
};

export default Register; 