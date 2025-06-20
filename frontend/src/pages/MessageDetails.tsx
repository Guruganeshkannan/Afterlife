import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    EnvelopeIcon,
    CalendarIcon,
    ChatBubbleLeftRightIcon,
    PencilIcon,
    TrashIcon,
} from '@heroicons/react/24/outline';
import { API_URL } from '../config';

interface Message {
    id: number;
    title: string;
    content: string;
    delivery_date: string;
    is_delivered: boolean;
    delivery_method: string;
    recipient_email: string;
    recipient_phone: string;
    personality_profile: Record<string, any>;
    generation_settings: {
        tone: string;
        length: string;
        style: string;
    };
}

const MessageDetails = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [message, setMessage] = useState<Message | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState<Partial<Message>>({});

    useEffect(() => {
        fetchMessage();
    }, [id, navigate]);

    const fetchMessage = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            const response = await fetch(`${API_URL}/messages/${id}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch message');
            }

            const data = await response.json();
            setMessage(data);
            setFormData(data);
        } catch (error) {
            console.error('Error fetching message:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdate = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('No authentication token');
            }

            const response = await fetch(`${API_URL}/messages/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Failed to update message');
            }

            const updatedMessage = await response.json();
            setMessage(updatedMessage);
            setIsEditing(false);
        } catch (err) {
            setError('Failed to update message. Please try again.');
        }
    };

    const handleDelete = async () => {
        if (!window.confirm('Are you sure you want to delete this message?')) {
            return;
        }

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            const response = await fetch(`${API_URL}/messages/${id}`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to delete message');
            }

            navigate('/dashboard');
        } catch (err) {
            setError('Failed to delete message. Please try again.');
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    if (!message) {
        return (
            <div className="text-center py-12">
                <h2 className="text-2xl font-semibold text-gray-900">Message not found</h2>
                <p className="mt-2 text-gray-600">The message you're looking for doesn't exist.</p>
            </div>
        );
    }

    return (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white shadow sm:rounded-lg"
            >
                <div className="px-4 py-5 sm:p-6">
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-2xl font-bold text-gray-900">{message.title}</h1>
                        <div className="flex space-x-3">
                            <button
                                onClick={() => setIsEditing(!isEditing)}
                                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                            >
                                <PencilIcon className="h-4 w-4 mr-2" />
                                {isEditing ? 'Cancel' : 'Edit'}
                            </button>
                            <button
                                onClick={handleDelete}
                                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                            >
                                <TrashIcon className="h-4 w-4 mr-2" />
                                Delete
                            </button>
                        </div>
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
                            onSubmit={handleUpdate}
                            className="space-y-6"
                        >
                            <div>
                                <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                                    Title
                                </label>
                                <div className="mt-1">
                                    <input
                                        type="text"
                                        name="title"
                                        id="title"
                                        required
                                        className="input-field"
                                        value={formData.title}
                                        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                    />
                                </div>
                            </div>

                            <div>
                                <label htmlFor="content" className="block text-sm font-medium text-gray-700">
                                    Content
                                </label>
                                <div className="mt-1">
                                    <textarea
                                        id="content"
                                        name="content"
                                        rows={6}
                                        required
                                        className="input-field"
                                        value={formData.content}
                                        onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                                    />
                                </div>
                            </div>

                            <div>
                                <label htmlFor="delivery_date" className="block text-sm font-medium text-gray-700">
                                    Delivery Date
                                </label>
                                <div className="mt-1">
                                    <input
                                        type="datetime-local"
                                        name="delivery_date"
                                        id="delivery_date"
                                        required
                                        className="input-field"
                                        value={formData.delivery_date}
                                        onChange={(e) => setFormData({ ...formData, delivery_date: e.target.value })}
                                    />
                                </div>
                            </div>

                            <div>
                                <label htmlFor="recipient_email" className="block text-sm font-medium text-gray-700">
                                    Recipient Email
                                </label>
                                <div className="mt-1">
                                    <input
                                        type="email"
                                        name="recipient_email"
                                        id="recipient_email"
                                        required
                                        className="input-field"
                                        value={formData.recipient_email}
                                        onChange={(e) => setFormData({ ...formData, recipient_email: e.target.value })}
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
                            <div className="prose max-w-none">
                                <p className="text-gray-700 whitespace-pre-wrap">{message.content}</p>
                            </div>

                            <div className="border-t border-gray-200 pt-6">
                                <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                                    <div className="sm:col-span-1">
                                        <dt className="text-sm font-medium text-gray-500">Delivery Date</dt>
                                        <dd className="mt-1 text-sm text-gray-900">
                                            {new Date(message.delivery_date).toLocaleString()}
                                        </dd>
                                    </div>
                                    <div className="sm:col-span-1">
                                        <dt className="text-sm font-medium text-gray-500">Status</dt>
                                        <dd className="mt-1 text-sm text-gray-900">
                                            <span
                                                className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${message.is_delivered
                                                    ? 'bg-green-100 text-green-800'
                                                    : 'bg-yellow-100 text-yellow-800'
                                                    }`}
                                            >
                                                {message.is_delivered ? 'Delivered' : 'Pending'}
                                            </span>
                                        </dd>
                                    </div>
                                    <div className="sm:col-span-1">
                                        <dt className="text-sm font-medium text-gray-500">Recipient</dt>
                                        <dd className="mt-1 text-sm text-gray-900">
                                            <div className="flex items-center">
                                                <EnvelopeIcon className="h-5 w-5 mr-2 text-gray-400" />
                                                {message.recipient_email}
                                            </div>
                                        </dd>
                                    </div>
                                    <div className="sm:col-span-1">
                                        <dt className="text-sm font-medium text-gray-500">Delivery Method</dt>
                                        <dd className="mt-1 text-sm text-gray-900">
                                            <div className="flex items-center">
                                                <ChatBubbleLeftRightIcon className="h-5 w-5 mr-2 text-gray-400" />
                                                {message.delivery_method.charAt(0).toUpperCase() + message.delivery_method.slice(1)}
                                            </div>
                                        </dd>
                                    </div>
                                </dl>
                            </div>
                        </motion.div>
                    )}
                </div>
            </motion.div>
        </div>
    );
};

export default MessageDetails; 