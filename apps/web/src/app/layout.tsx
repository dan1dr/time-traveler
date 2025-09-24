import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Time Traveler — Call the Past and Future',
  description: 'Initiate a live call with an era-flavored ElevenLabs agent via Twilio.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
      </head>
      <body>{children}</body>
    </html>
  )
}


