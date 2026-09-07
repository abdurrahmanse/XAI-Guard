import { redirect } from "next/navigation";

export default function AdminHome() {
  // For now, redirect overview to models page
  redirect("/models");
}
