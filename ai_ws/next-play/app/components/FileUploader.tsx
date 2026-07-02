
'use client'

import React from "react";

export default function FolderUpload() {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = Array.from(e.target.files || []);

        const allowedExtensions = [".txt", ".csv", ".json"];

        const validFiles = files.filter((file) =>
            allowedExtensions.some((ext) =>
                file.name.toLowerCase().endsWith(ext)
            )
        );

        console.log("Valid files:", validFiles);

        const rejectedFiles = files.filter(
            (file) =>
                !allowedExtensions.some((ext) =>
                    file.name.toLowerCase().endsWith(ext)
                )
        );

        console.log("Rejected files:", rejectedFiles);
    };
    const folderAttributes = {
        webkitdirectory: "",
        directory: ""
    };
    return (
        <input
            type="file"
            multiple
            {
            ...folderAttributes
            }// Crucial for folder upload
            onChange={handleChange}
        />
    );
}


