import React from 'react';
import { IoAlertCircle, IoWarning, IoClose } from 'react-icons/io5';

export function ErrorBanner({ type = 'error', message, onDismiss }) {
    const isError = type === 'error';
    const bgColor = isError ? 'bg-error-container/20' : 'bg-yellow-500/20';
    const borderColor = isError ? 'border-l-error' : 'border-l-yellow-500';
    const Icon = isError ? IoAlertCircle : IoWarning;
    const iconColor = isError ? 'text-error' : 'text-yellow-500';

    return (
        <div className={`glass-card flex items-start justify-between p-md mb-lg border-l-4 ${borderColor} ${bgColor} animate-fade-up`}>
            <div className="flex items-start gap-sm">
                <Icon className={`text-[24px] flex-shrink-0 ${iconColor}`} />
                <p className="font-body-md text-body-md text-on-surface pt-1">{message}</p>
            </div>
            {onDismiss && (
                <button onClick={onDismiss} className="text-on-surface-variant hover:text-on-surface transition-colors p-1">
                    <IoClose className="text-[20px]" />
                </button>
            )}
        </div>
    );
}
