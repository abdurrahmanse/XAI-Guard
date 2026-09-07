import React from "react";
import { Mail, MessageSquare, MapPin } from "lucide-react";

export default function ContactPage() {
  return (
    <div className="flex-1 w-full max-w-7xl mx-auto px-6 py-24">
      <div className="text-center mb-16">
        <h1 className="text-4xl sm:text-6xl font-bold tracking-tight mb-6">Contact Our Team</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Whether you're looking for a custom enterprise deployment or have a technical question, we're here to help.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
        {/* Contact Form */}
        <div className="bg-card border shadow-lg rounded-3xl p-8">
          <h3 className="text-2xl font-bold mb-6">Send us a message</h3>
          <form className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">First Name</label>
                <input type="text" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:ring-2 focus:ring-primary outline-none" placeholder="Jane" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Last Name</label>
                <input type="text" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:ring-2 focus:ring-primary outline-none" placeholder="Smith" />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Work Email</label>
              <input type="email" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:ring-2 focus:ring-primary outline-none" placeholder="jane@enterprise.com" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Message</label>
              <textarea className="w-full h-32 p-3 rounded-md border bg-background text-sm focus:ring-2 focus:ring-primary outline-none resize-none" placeholder="How can we help your SOC team?"></textarea>
            </div>
            <button type="button" className="w-full h-10 bg-primary text-primary-foreground font-medium rounded-md hover:bg-primary/90 transition-colors">
              Submit Request
            </button>
          </form>
        </div>

        {/* Contact Info */}
        <div className="flex flex-col justify-center space-y-8">
          <div className="flex gap-4 items-start">
            <div className="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-500 flex items-center justify-center shrink-0">
              <Mail className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-xl font-bold mb-1">Email Sales</h4>
              <p className="text-muted-foreground mb-2">Speak to our specialized technical sales team.</p>
              <a href="mailto:sales@xaiguard.enterprise" className="text-primary font-medium hover:underline">sales@xaiguard.enterprise</a>
            </div>
          </div>
          
          <div className="flex gap-4 items-start">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center shrink-0">
              <MessageSquare className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-xl font-bold mb-1">Support</h4>
              <p className="text-muted-foreground mb-2">Already a customer? Access our 24/7 dedicated SOC support channel.</p>
              <a href="#" className="text-primary font-medium hover:underline">Open a ticket &rarr;</a>
            </div>
          </div>

          <div className="flex gap-4 items-start">
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-500 flex items-center justify-center shrink-0">
              <MapPin className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-xl font-bold mb-1">Global HQ</h4>
              <p className="text-muted-foreground">
                128 Cybersecurity Blvd.<br/>
                San Francisco, CA 94105<br/>
                United States
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
