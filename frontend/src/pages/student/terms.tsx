import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function TermsOfUse() {
    return (
        <div className="container mx-auto max-w-4xl py-10 px-4">
            <Card>
                <CardHeader>
                    <CardTitle className="text-4xl font-bold text-center">
                        Terms of Use
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
                        <h2 className="font-semibold text-base">1. Acceptance of Terms</h2>
                        <p>
                            StudentHub (“Platform”) is owned and operated by Nuhvin Global Services
                            Pvt. Ltd. (“Company”, “we”, “our”, “us”).
                        </p>
                        <p>
                            By accessing or using StudentHub, you agree to be legally bound by
                            these Terms of Use. If you do not agree, you must not access or use
                            the Platform.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">2. Eligibility</h2>
                        <ul className="list-disc pl-6">
                            <li>Registered student, institution representative, or authorized administrator</li>
                            <li>At least 13 years old (or local legal age for digital consent)</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">3. User Accounts</h2>
                        <ul className="list-disc pl-6">
                            <li>Provide accurate and complete registration information</li>
                            <li>Maintain confidentiality of login credentials</li>
                            <li>Accept responsibility for all activities under your account</li>
                        </ul>
                        <p>
                            Any unauthorized access or misuse must be reported immediately.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">4. Platform Usage Rules</h2>
                        <ul className="list-disc pl-6">
                            <li>Do not upload false, illegal, or offensive content</li>
                            <li>Do not attempt unauthorized system access</li>
                            <li>Do not disrupt platform services or data integrity</li>
                            <li>Do not share account credentials</li>
                        </ul>
                        <p>
                            Violations may result in account suspension, termination, or legal action.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">5. Daily Work Submissions</h2>
                        <p>
                            Students are solely responsible for the authenticity and accuracy
                            of uploaded academic content. StudentHub does not guarantee content
                            accuracy but maintains secure storage.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">6. Intellectual Property</h2>
                        <p>
                            All software, design, branding, and content are the exclusive
                            property of Nuhvin Global Services Pvt. Ltd. Reproduction or
                            distribution without written permission is prohibited.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">7. Account Suspension or Termination</h2>
                        <ul className="list-disc pl-6">
                            <li>Violation of these Terms</li>
                            <li>Platform misuse or abuse</li>
                            <li>Security threats or fraudulent activity</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">8. Limitation of Liability</h2>
                        <p>
                            StudentHub is provided on an “as-is” basis. We are not liable for
                            data loss, service interruptions, or unauthorized access beyond
                            reasonable security safeguards.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">9. Modifications</h2>
                        <p>
                            We may update these Terms at any time. Continued use of the Platform
                            signifies acceptance of updated Terms.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">10. Governing Law</h2>
                        <p>
                            These Terms are governed by the laws of India. All disputes shall be
                            subject to the exclusive jurisdiction of the courts of Hyderabad,
                            Telangana.
                        </p>
                    </section>

                    <section>
                        <h2 className="font-semibold text-base">11. Disclaimer</h2>
                        <p>
                            StudentHub is provided on an “as-is” and “as-available” basis.
                            Nuhvin Global Services Pvt. Ltd. makes no warranties regarding
                            accuracy, reliability, uninterrupted service, or academic outcomes.
                        </p>
                        <p>
                            Use of the Platform is at the user’s own risk.
                        </p>
                    </section>

                    <hr className="my-6" />

                    <section>
                        <h2 className="font-semibold text-base">Grievance Redressal Mechanism</h2>
                        <p>
                            In accordance with the Information Technology Act, 2000 and IT Rules,
                            2021, StudentHub provides a grievance redressal mechanism.
                        </p>

                        <ul className="list-disc pl-6 mt-2">
                            <li>Account access or misuse</li>
                            <li>Data privacy or security issues</li>
                            <li>Uploaded content disputes</li>
                            <li>Technical or service issues</li>
                        </ul>

                        <p className="mt-2">
                            <strong>Grievance Contact:</strong><br />
                            Email:
                                <strong>studenthub@nuhvin.com</strong>
                            
                        </p>

                        <p className="mt-2">
                            Grievances will be acknowledged within 24 hours and resolved within
                            15 working days, subject to complexity.
                        </p>
                    </section>
                    <section>
                        <h2 className="font-semibold mt-4 text-base">Resolution Timeline</h2>
                        <ul className="list-disc pl-6 mt-2">
                            <li>All grievances will be acknowledged within 24 hours.</li>
                            <li>We aim to resolve complaints within 15 working days.</li>
                        </ul>

                        <p className="mt-2">
                            If a grievance requires extended technical review, legal verification,
                            or third-party involvement, the resolution timeline may exceed 15 working
                            days. In such cases, the user will be notified of the delay along with
                            regular status updates until the matter is resolved.
                        </p>
                    </section>


                </CardContent>
            </Card>
        </div>
    );
}
