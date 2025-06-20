import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    ChatBubbleLeftRightIcon,
    ClockIcon,
    HeartIcon,
    SparklesIcon
} from '@heroicons/react/24/outline';

const features = [
    {
        name: 'AI-Powered Messages',
        description: 'Create personalized messages that capture your essence using advanced AI technology.',
        icon: SparklesIcon,
    },
    {
        name: 'Scheduled Delivery',
        description: 'Set the perfect time for your messages to be delivered to your loved ones.',
        icon: ClockIcon,
    },
    {
        name: 'Personal Touch',
        description: 'Add your personality through writing samples and voice recordings.',
        icon: HeartIcon,
    },
    {
        name: 'Multiple Formats',
        description: 'Choose from text, audio, or video messages to express yourself.',
        icon: ChatBubbleLeftRightIcon,
    },
];

const Home = () => {
    return (
        <div className="relative isolate">
            {/* Background gradient */}
            <div
                className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
                aria-hidden="true"
            >
                <div
                    className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-primary-200 to-secondary-200 opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
                    style={{
                        clipPath:
                            'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
                    }}
                />
            </div>

            {/* Hero section */}
            <div className="py-24 sm:py-32">
                <div className="mx-auto max-w-7xl px-6 lg:px-8">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="mx-auto max-w-2xl text-center"
                    >
                        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                            Leave a lasting legacy with{' '}
                            <span className="text-primary-600">AfterLife</span>
                        </h1>
                        <p className="mt-6 text-lg leading-8 text-gray-600">
                            Create meaningful messages that will be delivered to your loved ones after you're gone.
                            Our AI-powered platform helps you express your thoughts, feelings, and memories in a
                            personal and authentic way.
                        </p>
                        <div className="mt-10 flex items-center justify-center gap-x-6">
                            <Link
                                to="/register"
                                className="btn-primary"
                            >
                                Get started
                            </Link>
                            <Link
                                to="/about"
                                className="text-sm font-semibold leading-6 text-gray-900 hover:text-primary-600"
                            >
                                Learn more <span aria-hidden="true">→</span>
                            </Link>
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Features section */}
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-2xl lg:text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                    >
                        <h2 className="text-base font-semibold leading-7 text-primary-600">Create Lasting Memories</h2>
                        <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                            Everything you need to preserve your legacy
                        </p>
                        <p className="mt-6 text-lg leading-8 text-gray-600">
                            Our platform combines cutting-edge AI technology with human touch to help you create
                            meaningful messages that will be cherished by your loved ones.
                        </p>
                    </motion.div>
                </div>
                <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
                    <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-4">
                        {features.map((feature, index) => (
                            <motion.div
                                key={feature.name}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5, delay: 0.1 * index }}
                            >
                                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                                    <feature.icon className="h-5 w-5 flex-none text-primary-600" aria-hidden="true" />
                                    {feature.name}
                                </dt>
                                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                                    <p className="flex-auto">{feature.description}</p>
                                </dd>
                            </motion.div>
                        ))}
                    </dl>
                </div>
            </div>

            {/* CTA section */}
            <div className="relative isolate mt-32 px-6 py-32 sm:mt-56 sm:py-40 lg:px-8">
                <div
                    className="absolute inset-x-0 top-1/2 -z-10 -translate-y-1/2 transform-gpu overflow-hidden opacity-30 blur-3xl"
                    aria-hidden="true"
                >
                    <div
                        className="ml-[max(50%,38rem)] aspect-[1313/771] w-[82.0625rem] bg-gradient-to-tr from-primary-200 to-secondary-200"
                        style={{
                            clipPath:
                                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
                        }}
                    />
                </div>
                <div className="mx-auto max-w-2xl text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.4 }}
                    >
                        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                            Ready to start your journey?
                        </h2>
                        <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-600">
                            Join thousands of users who are preserving their legacy with AfterLife.
                        </p>
                        <div className="mt-10 flex items-center justify-center gap-x-6">
                            <Link
                                to="/register"
                                className="btn-primary"
                            >
                                Create your first message
                            </Link>
                            <Link
                                to="/contact"
                                className="text-sm font-semibold leading-6 text-gray-900 hover:text-primary-600"
                            >
                                Contact us <span aria-hidden="true">→</span>
                            </Link>
                        </div>
                    </motion.div>
                </div>
            </div>
        </div>
    );
};

export default Home; 