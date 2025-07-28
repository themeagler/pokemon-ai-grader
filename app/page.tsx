"use client";

import { useState } from "react";

export default function Home() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">Pokémon AI Grader</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        className="mb-4 px-4 py-2 border border-gray-400 rounded cursor-pointer bg-white text-black"
      />

      {previewUrl && (
        <div className="shadow-md rounded-lg p-4 bg-white">
          <p className="mb-2 font-semibold">Preview:</p>
          <img
            src={previewUrl}
            alt="Card preview"
            className="max-w-xs border border-gray-300 rounded"
          />
        </div>
      )}
    </main>
  );
}



