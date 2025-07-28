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
    <main style={{ backgroundColor: "#f3f4f6", minHeight: "100vh", padding: "2rem", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
      <h1 style={{ fontSize: "2rem", fontWeight: "bold", marginBottom: "1rem" }}>Pokémon AI Grader</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        style={{
          padding: "10px",
          backgroundColor: "#fff",
          color: "#000",
          border: "2px solid #333",
          borderRadius: "5px",
          cursor: "pointer",
          marginBottom: "20px"
        }}
      />

      {previewUrl && (
        <div style={{ backgroundColor: "#fff", padding: "1rem", borderRadius: "8px", boxShadow: "0 2px 6px rgba(0,0,0,0.1)" }}>
          <p style={{ fontWeight: "bold", marginBottom: "0.5rem" }}>Preview:</p>
          <img
            src={previewUrl}
            alt="Card preview"
            style={{ maxWidth: "300px", border: "1px solid #ccc", borderRadius: "4px" }}
          />
        </div>
      )}
    </main>
  );
}



