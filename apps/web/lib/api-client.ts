export class ApiClient {
  static async get(endpoint: string) {
    const res = await fetch(`/api/proxy${endpoint}`);
    if (!res.ok) throw new Error("API request failed");
    return res.json();
  }
  
  static async post(endpoint: string, data: any) {
    const res = await fetch(`/api/proxy${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("API request failed");
    return res.json();
  }
}
