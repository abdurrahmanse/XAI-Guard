import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex h-[70vh] flex-col items-center justify-center space-y-4">
      <h2 className="text-4xl font-bold tracking-tight">404</h2>
      <p className="text-xl text-gray-500">Page not found</p>
      <p className="text-sm text-gray-400 max-w-[400px] text-center mb-8">
        The page you are looking for does not exist or has been moved.
      </p>
      <Link href="/">
        <button className="px-4 py-2 bg-blue-600 text-white rounded">Return Home</button>
      </Link>
    </div>
  );
}
