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
      <body>{children}</body>
    </html>
  )
}


