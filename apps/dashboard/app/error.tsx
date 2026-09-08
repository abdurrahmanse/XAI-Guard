'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('App Error:', error);
  }, [error]);

  return (
    <div className="flex h-[50vh] flex-col items-center justify-center space-y-4">
      <h2 className="text-2xl font-bold tracking-tight text-red-500">
        Something went wrong!
      </h2>
      <p className="text-gray-500 max-w-[500px] text-center">
        {error.message || "An unexpected error occurred in the dashboard."}
      </p>
      <div className="flex space-x-4">
        <button onClick={() => reset()} className="px-4 py-2 bg-blue-600 text-white rounded">
          Try again
        </button>
        <button onClick={() => window.location.href = '/'} className="px-4 py-2 border border-gray-300 rounded">
          Return Home
        </button>
      </div>
    </div>
  );
}
