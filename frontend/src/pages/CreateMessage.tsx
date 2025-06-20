import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    EnvelopeIcon,
    CalendarIcon,
    ChatBubbleLeftRightIcon,
    PhotoIcon,
    MicrophoneIcon,
    VideoCameraIcon,
} from '@heroicons/react/24/outline';
import { API_URL } from '../config';

const CreateMessage = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        title: '',
        content: '',
        delivery_date: '',
        delivery_method: 'email',
        recipient_email: '',
        recipient_phone: '',
        personality_profile: {},
        generation_settings: {
            tone: 'warm',
            length: 'medium',
            style: 'personal',
        },
    });
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsSubmitting(true);

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            const response = await fetch(`${API_URL}/messages/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Failed to create message');
            }

            navigate('/dashboard');
        } catch (err) {
            setError('Failed to create message. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mb-8"
            >
                <h1 className="text-3xl font-bold text-gray-900">Create a New Message</h1>
                <p className="mt-2 text-sm text-gray-600">
                    Craft a meaningful message that will be delivered to your loved ones.
                </p>
            </motion.div>

            <motion.form
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                onSubmit={handleSubmit}
                className="space-y-8"
            >
                <div className="bg-white shadow sm:rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <h3 className="text-lg font-medium leading-6 text-gray-900">Message Details</h3>
                        <div className="mt-5 space-y-6">
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
                                    Message Content
                                </label>
                                <div className="mt-1">
                                    <textarea
                                        id="content"
                                        name="content"
                                        rows={4}
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
                                <div className="mt-1 relative rounded-md shadow-sm">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <CalendarIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                    </div>
                                    <input
                                        type="datetime-local"
                                        name="delivery_date"
                                        id="delivery_date"
                                        required
                                        className="input-field pl-10"
                                        value={formData.delivery_date}
                                        onChange={(e) => setFormData({ ...formData, delivery_date: e.target.value })}
                                    />
                                </div>
                            </div>

                            <div>
                                <label htmlFor="delivery_method" className="block text-sm font-medium text-gray-700">
                                    Delivery Method
                                </label>
                                <div className="mt-1">
                                    <select
                                        id="delivery_method"
                                        name="delivery_method"
                                        className="input-field"
                                        value={formData.delivery_method}
                                        onChange={(e) => setFormData({ ...formData, delivery_method: e.target.value })}
                                    >
                                        <option value="email">Email</option>
                                        <option value="sms">SMS</option>
                                        <option value="both">Both Email and SMS</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <label htmlFor="recipient_email" className="block text-sm font-medium text-gray-700">
                                    Recipient Email
                                </label>
                                <div className="mt-1 relative rounded-md shadow-sm">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <EnvelopeIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                    </div>
                                    <input
                                        type="email"
                                        name="recipient_email"
                                        id="recipient_email"
                                        required
                                        className="input-field pl-10"
                                        value={formData.recipient_email}
                                        onChange={(e) => setFormData({ ...formData, recipient_email: e.target.value })}
                                    />
                                </div>
                            </div>

                            {(formData.delivery_method === 'sms' || formData.delivery_method === 'both') && (
                                <div>
                                    <label htmlFor="recipient_phone" className="block text-sm font-medium text-gray-700">
                                        Recipient Phone Number
                                    </label>
                                    <div className="mt-1">
                                        <input
                                            type="tel"
                                            name="recipient_phone"
                                            id="recipient_phone"
                                            className="input-field"
                                            value={formData.recipient_phone}
                                            onChange={(e) => setFormData({ ...formData, recipient_phone: e.target.value })}
                                        />
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <div className="bg-white shadow sm:rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                        <h3 className="text-lg font-medium leading-6 text-gray-900">Message Style</h3>
                        <div className="mt-5 space-y-6">
                            <div>
                                <label htmlFor="tone" className="block text-sm font-medium text-gray-700">
                                    Tone
                                </label>
                                <div className="mt-1">
                                    <select
                                        id="tone"
                                        name="tone"
                                        className="input-field"
                                        value={formData.generation_settings.tone}
                                        onChange={(e) =>
                                            setFormData({
                                                ...formData,
                                                generation_settings: {
                                                    ...formData.generation_settings,
                                                    tone: e.target.value,
                                                },
                                            })
                                        }
                                    >
                                        <option value="warm">Warm and Loving</option>
                                        <option value="formal">Formal and Professional</option>
                                        <option value="casual">Casual and Friendly</option>
                                        <option value="humorous">Humorous and Playful</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <label htmlFor="length" className="block text-sm font-medium text-gray-700">
                                    Length
                                </label>
                                <div className="mt-1">
                                    <select
                                        id="length"
                                        name="length"
                                        className="input-field"
                                        value={formData.generation_settings.length}
                                        onChange={(e) =>
                                            setFormData({
                                                ...formData,
                                                generation_settings: {
                                                    ...formData.generation_settings,
                                                    length: e.target.value,
                                                },
                                            })
                                        }
                                    >
                                        <option value="short">Short and Concise</option>
                                        <option value="medium">Medium</option>
                                        <option value="long">Long and Detailed</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <label htmlFor="style" className="block text-sm font-medium text-gray-700">
                                    Style
                                </label>
                                <div className="mt-1">
                                    <select
                                        id="style"
                                        name="style"
                                        className="input-field"
                                        value={formData.generation_settings.style}
                                        onChange={(e) =>
                                            setFormData({
                                                ...formData,
                                                generation_settings: {
                                                    ...formData.generation_settings,
                                                    style: e.target.value,
                                                },
                                            })
                                        }
                                    >
                                        <option value="personal">Personal and Intimate</option>
                                        <option value="story">Story-like</option>
                                        <option value="letter">Letter Format</option>
                                        <option value="poetic">Poetic</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {error && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="rounded-md bg-red-50 p-4"
                    >
                        <div className="text-sm text-red-700">{error}</div>
                    </motion.div>
                )}

                <div className="flex justify-end space-x-4">
                    <button
                        type="button"
                        onClick={() => navigate('/dashboard')}
                        className="btn-secondary"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        disabled={isSubmitting}
                        className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isSubmitting ? 'Creating...' : 'Create Message'}
                    </button>
                </div>
            </motion.form>
        </div>
    );
};

export default CreateMessage; 