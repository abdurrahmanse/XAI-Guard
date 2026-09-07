for app in web dashboard admin; do
  layout_file="apps/$app/app/layout.tsx"
  
  # Insert the import after the first line (which is usually import "./globals.css";)
  sed -i '' '/import ".\/globals.css";/a\
import { Inter } from "next/font/google";\
const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });\
' $layout_file

  # Replace <html lang="en" suppressHydrationWarning> with <html lang="en" className={inter.variable} suppressHydrationWarning>
  sed -i '' 's/<html lang="en" suppressHydrationWarning>/<html lang="en" className={inter.variable} suppressHydrationWarning>/g' $layout_file
  
  # Ensure the body uses antialiased and font-sans
  sed -i '' 's/<body className="/<body className="antialiased font-sans /g' $layout_file
done
