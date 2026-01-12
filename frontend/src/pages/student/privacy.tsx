import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function PrivacyPolicy() {
    return (
        <div className="container mx-auto max-w-4xl py-10 px-4">
            <Card>
                <CardHeader>
                    <CardTitle className="text-4xl font-bold text-center">
                        Privacy Policy
                    </CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">
                        Effective Date: January 08, 2026
                    </p>
                    <p className="text-sm text-muted-foreground">
                        Owned & Operated by <img src="/logo.png" alt="Nuhvin Logo" className="inline h-10 w-12" />
                    </p>
                    <strong>Nuhvin Global Services Pvt. Ltd.</strong>
                    <p className="text-sm text-muted-foreground">
                        www.nuhvin.com
                    </p>
                </CardHeader>

                <CardContent className="space-y-6 text-sm leading-relaxed">

                    <section>
                        <h2 className="font-semibold text-base">1. Information We Collect</h2>
                        <ul className="list-disc pl-6">
                            <li>Personal details (name, email, contact number, institution, etc.)</li>
                            <li>Login credentials (securely encrypted)</li>
                            <li>Academic data & uploads</li>
                            <li>Usage analytics & system logs</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">2. Purpose of Data Collection</h2>
                        <p>Your information is used to:</p>
                        <ul className="list-disc pl-6">
                            <li>Provide and manage academic services</li>
                            <li>Maintain user accounts</li>
                            <li>Improve platform quality and security</li>
                            <li>Communicate important updates</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">3. Data Protection & Security</h2>
                        <p>We implement:</p>
                        <ul className="list-disc pl-6">
                            <li>Encryption</li>
                            <li>Access controls</li>
                            <li>Secure servers</li>
                            <li>Continuous monitoring</li>
                        </ul>
                        <p>
                            Your information is protected against unauthorized access and misuse.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">4. Data Sharing</h2>
                        <p>We do not sell or rent personal information.</p>
                        <p>Data may be shared only:</p>
                        <ul className="list-disc pl-6">
                            <li>With authorized institution administrators</li>
                            <li>When legally required by law enforcement</li>
                            <li>To protect company rights and platform integrity</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">5. Cookies & Tracking</h2>
                        <p>We use cookies to:</p>
                        <ul className="list-disc pl-6">
                            <li>Maintain login sessions</li>
                            <li>Improve user experience</li>
                            <li>Analyze platform usage</li>
                        </ul>
                        <p>You may disable cookies in your browser settings.</p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">6. User Rights</h2>
                        <p>Users may:</p>
                        <ul className="list-disc pl-6">
                            <li>Access your data</li>
                            <li>Request correction of errors</li>
                            <li>Request deletion of your account and personal data</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">7. Data Retention</h2>
                        <p>
                            Data is retained only as long as required for educational, legal, and
                            operational purposes.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">8. Third-Party Services</h2>
                        <p>
                            We may integrate compliant third-party providers for hosting,
                            communication, email, analytics, and storage.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">9. Policy Updates</h2>
                        <p>
                            Policy updates will be posted on this page. Continued usage indicates
                            acceptance.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">10. Contact Information</h2>
                        <p>
                            <strong>Nuhvin Global Services Pvt. Ltd.</strong><br />
                            Website: www.nuhvin.com<br />
                            Email: <strong>studenthub@nuhvin.com</strong>
                        </p>
                    </section>

                </CardContent>
            </Card>
        </div>
    );
}
