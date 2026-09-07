for app in web dashboard admin; do
  sed -i '' 's/@import "tailwindcss";/@import "tailwindcss";\n@source "..\/..\/packages\/ui";/g' apps/$app/app/globals.css
done
