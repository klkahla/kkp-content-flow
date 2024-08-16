export async function createContentWorkflow(prompt: string, csvFilePath: string) {
    try {
        const requestBody = {
            prompt_message: prompt,
            csv_file_path: csvFilePath
        };
        
        const resp = await fetch(
            "http://127.0.0.1:8000/content-workflow",
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            }
        );
        if (!resp.ok) {
            const errorText = await resp.text()
            console.error('Error response: ', errorText);
            throw new Error('Failed to finish content creation workflow');
        }

        const responseData = await resp.json(); 
        return responseData;
    } catch (error) {
        console.error('Error in content creation workflow:', error);
        throw error;
    }
}