// import React, { useState } from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import { useForm } from 'react-hook-form';
// import { zodResolver } from '@hookform/resolvers/zod';
// import { z } from 'zod';
// import { Eye, EyeOff, Loader2, ChevronLeft, ChevronRight } from 'lucide-react';
// import { Button } from '@/components/ui/button';
// import { Input } from '@/components/ui/input';
// import { Label } from '@/components/ui/label';
// import { useToast } from '@/hooks/use-toast';
// import { useAuth } from '@/contexts/AuthContext';
// import AuthLayout from '@/components/auth/AuthLayout';

// const signupSchema = z.object({
//   firstName: z.string().min(1, 'First name is required').max(50),
//   lastName: z.string().min(1, 'Last name is required').max(50),
//   email: z.string().email('Please enter a valid email address'),
//   contactNumber: z.string().min(10, 'Please enter a valid phone number').max(15),
//   collegeName: z.string().min(3, 'College name is required').max(100),
//   address: z.string().min(3, 'College address is required').max(200),
//   collegeEmail: z.string().email('Invalid college email').optional().or(z.literal('')),
//   city: z.string().min(2, 'City is required').max(100),
//   pincode: z.string().length(6, 'Pincode must be 6 digits').regex(/^\d+$/, 'Pincode must contain only numbers'),
//   courseName: z.string().min(2, 'Course name is required').max(100),
//   courseMode: z.enum(['online', 'offline'], {
//   required_error: 'Course mode is required',
//   invalid_type_error: 'Course mode is required',
// }),

// courseDuration: z.enum(['long', 'short'], {
//   required_error: 'Course duration is required',
//   invalid_type_error: 'Course duration is required',
// }),

//   emailOtp: z.string().min(4, 'OTP is required'),

//   password: z.string()
//     .min(8, 'Password must be at least 8 characters')
//     .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
//     .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
//     .regex(/[0-9]/, 'Password must contain at least one number'),
//   confirmPassword: z.string(),
// }).refine((data) => data.password === data.confirmPassword, {
//   message: "Passwords don't match",
//   path: ['confirmPassword'],
// });

// type SignupFormData = z.infer<typeof signupSchema>;

// const SignupPage: React.FC = () => {
//   const [step, setStep] = useState(1);
//   const [showPassword, setShowPassword] = useState(false);
//   const [showConfirmPassword, setShowConfirmPassword] = useState(false);
//   const [isLoading, setIsLoading] = useState(false);
//   const [otpSent, setOtpSent] = useState(false);
//   const [email, setEmail] = useState('');
//   const { signUp } = useAuth();
//   const { toast } = useToast();
//   const navigate = useNavigate();

//   const {
//     register,
//     handleSubmit,
//     trigger,
//     getValues,
//     formState: { errors },
//   } = useForm<SignupFormData>({
//     resolver: zodResolver(signupSchema),
//     mode: 'onBlur',
//   });

//   const step1Fields = ['firstName', 'lastName', 'email', 'contactNumber'] as const;
//   const step2Fields = ['collegeName', 'address', 'city', 'pincode', 'collegeEmail'] as const;
//   const step3Fields = ['courseName', 'courseMode', 'courseDuration'] as const;
//   const step4Fields = ['emailOtp','password', 'confirmPassword'] as const;

//   const handleSendOtp = async () => {
//     const email = getValues('email');
//     if (!email) {
//       toast({
//         variant: 'destructive',
//         title: 'Email required',
//         description: 'Please enter your email address first.',
//       });
//       return;
//     }

//     setIsLoading(true);
//     try {
//       const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/auth/send-signup-otp`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ email }),
//       });

//       const result = await response.json();
//       if (result.success) {
//         setOtpSent(true);
//         setEmail(email);
//         toast({
//           title: 'OTP Sent',
//           description: 'Check your email for the verification code.',
//         });
//       }
//     } catch (error) {
//       toast({
//         variant: 'destructive',
//         title: 'Error',
//         description: 'Failed to send OTP. Please try again.',
//       });
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleNext = async () => {
//     let fieldsToValidate: ReadonlyArray<keyof SignupFormData> = [];
//     if (step === 1) fieldsToValidate = step1Fields;
//     if (step === 2) fieldsToValidate = step2Fields;
//     if (step === 3) fieldsToValidate = step3Fields;

//     const isValid = await trigger(fieldsToValidate);
//     if (isValid) {
//       setStep(step + 1);
//     }
//   };

//   const handleBack = () => {
//     if (step === 4) {
//       setOtpSent(false);
//     }
//     setStep(step - 1);
//   };

//   const onSubmit = async (data: SignupFormData) => {
//     setIsLoading(true);
//     try {
//       const result = await signUp(data.email, data.password, {
//         full_name: `${data.firstName} ${data.lastName}`,
//         contact_number: data.contactNumber,
//         college_name: data.collegeName,
//         address: data.address,
//         city: data.city,
//         pincode: data.pincode,
//         college_email: data.collegeEmail || '',
//         course_name: data.courseName,
//         course_mode: data.courseMode,
//         course_duration: data.courseDuration,
//         emailOtp: data.emailOtp,
//       });

//       if (result.success) {
//         toast({
//           title: 'Registration successful!',
//           description: 'Your account is pending approval. You will be notified once approved.',
//         });
//         navigate('/auth/pending-approval');
//       } else {
//         toast({
//           title: 'Registration failed',
//           description: result.message,
//           variant: 'destructive',
//         });
//       }
//     } catch (error) {
//       toast({
//         title: 'Error',
//         description: 'An unexpected error occurred. Please try again.',
//         variant: 'destructive',
//       });
//     } finally {
//       setIsLoading(false);
//     }
//   };
  

//   const renderStepIndicator = () => (
//     <div className="flex items-center justify-center gap-2 mb-8">
//       {[1, 2, 3,4].map((s) => (
//         <React.Fragment key={s}>
//           <div
//             className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${s === step
//                 ? 'bg-primary text-primary-foreground'
//                 : s < step
//                   ? 'bg-success text-success-foreground'
//                   : 'bg-muted text-muted-foreground'
//               }`}
//           >
//             {s}
//           </div>
//           {s < 4 && (
//             <div className={`w-12 h-1 rounded ${s < step ? 'bg-success' : 'bg-muted'}`} />
//           )}
//         </React.Fragment>
//       ))}
//     </div>
//   );
  

//   return (
//     <AuthLayout
//       title="Create an account"
//       subtitle={
//         step === 1 ? "Let's start with your personal details" :
//           step === 2 ? "Tell us about your college" :
//             "Create a secure password"
//       }
//     >
//       {renderStepIndicator()}

//       <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
//         {step === 1 && (
//           <div className="space-y-4 animate-fade-in">
//             <div className="space-y-2">
//               <Label htmlFor="firstName">First Name</Label>
//               <Input
//                 id="firstName"
//                 placeholder="Enter your First Name"
//                 {...register('firstName')}
//                 className={errors.firstName ? 'border-destructive' : ''}
//               />
//               {errors.firstName && (
//                 <p className="text-xs text-destructive">{errors.firstName.message}</p>
//               )}
//             </div>
//             <div className="space-y-2">
//               <Label htmlFor="lastName">Last name</Label>
//               <Input
//                 id="lastName"
//                 placeholder="Enter your Last Name"
//                 {...register('lastName')}
//                 className={errors.lastName ? 'border-destructive' : ''}
//               />
//               {errors.lastName && (
//                 <p className="text-xs text-destructive">{errors.lastName.message}</p>
//               )}
//             </div>

//             <div className="space-y-2">
//               <Label htmlFor="email">Email Address</Label>
//               <Input
//                 id="email"
//                 type="email"
//                 placeholder="Enter the Email Address"
//                 {...register('email')}
//                 className={errors.email ? 'border-destructive' : ''}
//               />
//               {errors.email && (
//                 <p className="text-xs text-destructive">{errors.email.message}</p>
//               )}
//             </div>

//             <div className="space-y-2">
//               <Label htmlFor="contactNumber">Contact Number</Label>
            
//               <Input
//                 id="contactNumber"
//                 type="tel"
//                 placeholder="Enter your Mobile Number"
//                 maxLength={10}
//                 minLength={10}
//                 {...register('contactNumber')}
//                 className={errors.contactNumber ? 'border-destructive' : ''}
//               />
//               {errors.contactNumber && (
//                 <p className="text-xs text-destructive">{errors.contactNumber.message}</p>
//               )}
//             </div>
//           </div>
//         )}

//         {step === 2 && (
//           <div className="space-y-4 animate-fade-in">

//             <div className="space-y-2">
//               <Label htmlFor="collegeName">College Name</Label>
//               <Input
//                 id="collegeName"
//                 placeholder="Enter your College Name"
//                 {...register('collegeName')}
//                 className={errors.collegeName ? 'border-destructive' : ''}
//               />
//               {errors.collegeName && (
//                 <p className="text-xs text-destructive">{errors.collegeName.message}</p>
//               )}
//             </div>

//             <div className="space-y-2">
//               <Label htmlFor="address">Address</Label>
//               <Input
//                 id="address"
//                 type="text"
//                 placeholder="Enter your Address"
//                 {...register('address')}
//                 className={errors.address ? 'border-destructive' : ''}
//               />
//               {errors.address && (
//                 <p className="text-xs text-destructive">{errors.address.message}</p>
//               )}
//             </div>

//             <div className="space-y-2 flex flex-col sm:flex-row w-full">
//               <div className='sm:w-1/2 w-full sm:mr-3 pt-2'>
//                 <Label htmlFor="city">City</Label>
//                 <Input
//                   id="city"
//                   type='text'
//                   minLength={2}
//                   placeholder="Enter your City"
//                   {...register('city')}
//                   className={errors.city ? 'border-destructive' : ''}
//                 />
//                 {errors.city && (
//                   <p className="text-xs text-destructive">{errors.city.message}</p>
//                 )}
//               </div>

//               <div className='sm:w-1/2 w-full'>
//                 <Label htmlFor="pincode">Pincode</Label>
//                 <Input
//                   id="pincode"
//                   type='tel'
//                   maxLength={6}
//                   minLength={6}
//                   placeholder="Enter the pincode"
//                   {...register('pincode')}
//                   className={errors.pincode ? 'border-destructive' : ''}
//                 />
//                 {errors.pincode && (
//                   <p className="text-xs text-destructive">{errors.pincode.message}</p>
//                 )}
//               </div>
//             </div>
//           </div>
//         )}
//         { step === 3 && (
//           <div className="space-y-4 animate-fade-in">
//             <div className="space-y-2">
//               <Label htmlFor="courseName">Course Name</Label>
//               <Input
//                 id="courseName"
//                 type="text"
//                 placeholder="Enter your Course Name"
//                 {...register('courseName')}
//                 className={errors.courseName ? 'border-destructive' : ''}
//               />
//               {errors.courseName && (
//                 <p className="text-xs text-destructive">{errors.courseName.message}</p>
//               )}
//             </div>

//             <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
//               <div className="space-y-2">
//                 <Label htmlFor="courseMode">Course mode</Label>
//                 <select
//                   id="courseMode"
//                   {...register('courseMode')}
//                   className={`w-full border rounded px-3 py-2 ${errors.courseMode ? 'border-destructive' : ''}`}
//                 >
//                   <option value="">Select mode</option>
//                   <option value="online">Online</option>
//                   <option value="offline">Offline</option>
//                 </select>
//                 {errors.courseMode && (
//                   <p className="text-xs text-destructive">{String(errors.courseMode.message)}</p>
//                 )}
//               </div>

//               <div className="space-y-2">
//                 <Label htmlFor="courseDuration">Course duration</Label>
//                 <select
//                   id="courseDuration"
//                   {...register('courseDuration')}
//                   className={`w-full border rounded px-3 py-2 ${errors.courseDuration ? 'border-destructive' : ''}`}
//                 >
//                   <option value="">Select duration</option>
//                   <option value="long">Long Term</option>
//                   <option value="short">Short Term</option>
//                 </select>
//                 {errors.courseDuration && (
//                   <p className="text-xs text-destructive">{String(errors.courseDuration.message)}</p>
//                 )}
//               </div>
//             </div>
//           </div>
//         )}

//         {step === 4 && (
//           <div className="space-y-4 animate-fade-in">
//             {!otpSent && (
//               <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
//                 <p className="text-sm text-blue-900">
//                   We'll send a verification code to <strong>{email}</strong>
//                 </p>
//                 <Button
//                   type="button"
//                   onClick={handleSendOtp}
//                   disabled={isLoading}
//                   className="mt-3 w-full"
//                   variant="outline"
//                 >
//                   {isLoading ? (
//                     <>
//                       <Loader2 className="mr-2 h-4 w-4 animate-spin" />
//                       Sending...
//                     </>
//                   ) : (
//                     'Send Verification Code'
//                   )}
//                 </Button>
//               </div>
//             )}

//             {otpSent && (
//               <div className="space-y-2">
//                 <label htmlFor="emailOtp">Email Verification Code</label>
//                 <Input
//                   id="emailOtp"
//                   type="text"
//                   placeholder="Enter the 6-digit code sent to your email"
//                   {...register('emailOtp')}
//                   className={errors.emailOtp ? 'border-destructive' : ''}
//                   maxLength={6}
//                 />
//                 {errors.emailOtp && (
//                   <p className="text-xs text-destructive">{errors.emailOtp.message}</p>
//                 )}
//                 <Button
//                   type="button"
//                   onClick={handleSendOtp}
//                   disabled={isLoading}
//                   variant="link"
//                   className="p-0 h-auto text-xs"
//                 >
//                   Resend code
//                 </Button>
//               </div>
//             )}

//             <div className="space-y-2">
//               <Label htmlFor="password">Password</Label>
//               <div className="relative">
//                 <Input
//                   id="password"
//                   type={showPassword ? 'text' : 'password'}
//                   placeholder="Create a strong password"
//                   {...register('password')}
//                   className={errors.password ? 'border-destructive pr-10' : 'pr-10'}
//                 />
//                 <button
//                   type="button"
//                   onClick={() => setShowPassword(!showPassword)}
//                   className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
//                 >
//                   {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
//                 </button>
//               </div>
//               {errors.password && (
//                 <p className="text-xs text-destructive">{errors.password.message}</p>
//               )}
//               <p className="text-xs text-muted-foreground">
//                 At least 8 characters with uppercase, lowercase, and number
//               </p>
//             </div>

//             <div className="space-y-2">
//               <Label htmlFor="confirmPassword">Confirm Password</Label>
//               <div className="relative">
//                 <Input
//                   id="confirmPassword"
//                   type={showConfirmPassword ? 'text' : 'password'}
//                   placeholder="Re-enter your password"
//                   {...register('confirmPassword')}
//                   className={errors.confirmPassword ? 'border-destructive pr-10' : 'pr-10'}
//                 />
//                 <button
//                   type="button"
//                   onClick={() => setShowConfirmPassword(!showConfirmPassword)}
//                   className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
//                 >
//                   {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
//                 </button>
//               </div>
//               {errors.confirmPassword && (
//                 <p className="text-xs text-destructive">{errors.confirmPassword.message}</p>
//               )}
//             </div>
//           </div>
//         )}
        

//         <div className="flex flex-col sm:flex-row gap-3 pt-2">
//           {step > 1 && (
//             <Button type="button" variant="outline" onClick={handleBack} className="w-full sm:flex-1">
//               <ChevronLeft className="w-4 h-4" />
//               Back
//             </Button>
//           )}
//           {step < 4 ? (
//             <Button type="button" onClick={handleNext} className="w-full sm:flex-1">
//               Next
//               <ChevronRight className="w-4 h-4" />
//             </Button>
//           ) : (
//             <Button type="submit" className="w-full sm:flex-1" disabled={isLoading}>
//               {isLoading ? (
//                 <>
//                   <Loader2 className="w-4 h-4 animate-spin" />
//                   Creating account...
//                 </>
//               ) : (
//                 'Create account'
//               )}
//             </Button>
//           )}
//         </div>

//         <p className="text-center text-sm text-muted-foreground">
//           Already have an account?{' '}
//           <Link to="/auth/login" className="text-primary font-medium hover:text-primary/80">
//             Sign in
//           </Link>
//         </p>
//       </form>
//     </AuthLayout>
//   );
// };

// export default SignupPage;


import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Eye, EyeOff, Loader2, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/contexts/AuthContext';
import AuthLayout from '@/components/auth/AuthLayout';

/* =======================
   Schema
======================= */

const signupSchema = z.object({
  firstName: z.string().min(1, 'First name is required').max(50),
  lastName: z.string().min(1, 'Last name is required').max(50),
  email: z.string().email('Please enter a valid email address'),
  contactNumber: z.string().min(10, 'Please enter a valid phone number').max(15),
  collegeName: z.string().min(3, 'College name is required').max(100),
  address: z.string().min(3, 'College address is required').max(200),
  collegeEmail: z.string().email('Invalid college email').optional().or(z.literal('')),
  city: z.string().min(2, 'City is required').max(100),
  pincode: z.string().length(6, 'Pincode must be 6 digits').regex(/^\d+$/, 'Pincode must contain only numbers'),
  courseName: z.string().min(2, 'Course name is required').max(100),

  courseMode: z.enum(['online', 'offline'], {
    required_error: 'Course mode is required',
    invalid_type_error: 'Course mode is required',
  }),

  courseDuration: z.enum(['long', 'short'], {
    required_error: 'Course duration is required',
    invalid_type_error: 'Course duration is required',
  }),

  emailOtp: z.string().min(4, 'OTP is required'),

  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),

  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type SignupFormData = z.infer<typeof signupSchema>;

/* =======================
   Component
======================= */

const SignupPage: React.FC = () => {
  const [step, setStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [otpSent, setOtpSent] = useState(false);
  const [email, setEmail] = useState('');

  /* 🔹 NEW: added verifySignupOtp */
  const { signUp, verifySignupOtp } = useAuth();

  const { toast } = useToast();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    trigger,
    getValues,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
    mode: 'onBlur',
  });

  const step1Fields = ['firstName', 'lastName', 'email', 'contactNumber'] as const;
  const step2Fields = ['collegeName', 'address', 'city', 'pincode', 'collegeEmail'] as const;
  const step3Fields = ['courseName', 'courseMode', 'courseDuration'] as const;
  const step4Fields = ['emailOtp', 'password', 'confirmPassword'] as const;

  /* =======================
     Send OTP
  ======================= */

  const handleSendOtp = async () => {
  const formEmail = getValues('email');

  if (!formEmail) {
    toast({
      variant: 'destructive',
      title: 'Email required',
      description: 'Please enter your email address first.',
    });
    return;
  }

  setIsLoading(true);
  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/auth/send-signup-otp`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: formEmail }),
      }
    );

    const result = await response.json();

    if (result.success) {
      setOtpSent(true);
      setEmail(formEmail); // ✅ sync state AFTER success

      toast({
        title: 'OTP Sent',
        description: 'Check your email for the verification code.',
      });
    } else {
      toast({
        variant: 'destructive',
        title: 'Failed to send OTP',
        description: result.message || 'Unable to send OTP',
      });
    }
  } catch {
    toast({
      variant: 'destructive',
      title: 'Error',
      description: 'Failed to send OTP. Please try again.',
    });
  } finally {
    setIsLoading(false);
  }
};


  /* =======================
     Step Control
  ======================= */

  const handleNext = async () => {
    let fieldsToValidate: ReadonlyArray<keyof SignupFormData> = [];
    if (step === 1) fieldsToValidate = step1Fields;
    if (step === 2) fieldsToValidate = step2Fields;
    if (step === 3) fieldsToValidate = step3Fields;

    const isValid = await trigger(fieldsToValidate);
    if (isValid) setStep(step + 1);
  };

  const handleBack = () => {
    if (step === 4) setOtpSent(false);
    setStep(step - 1);
  };

  /* =======================
     Submit (UPDATED)
  ======================= */

  const onSubmit = async (data: SignupFormData) => {
    setIsLoading(true);
    try {
      /* 🔹 NEW: verify OTP before signup */
      const otpResult = await verifySignupOtp(data.email, data.emailOtp);
      if (!otpResult.success) {
        toast({
          variant: 'destructive',
          title: 'OTP verification failed',
          description: otpResult.message,
        });
        setIsLoading(false);
        return;
      }

      const result = await signUp(data.email, data.password, {
        full_name: `${data.firstName} ${data.lastName}`,
        contact_number: data.contactNumber,
        college_name: data.collegeName,
        address: data.address,
        city: data.city,
        pincode: data.pincode,
        college_email: data.collegeEmail || '',
        course_name: data.courseName,
        course_mode: data.courseMode,
        course_duration: data.courseDuration,
        emailOtp: data.emailOtp,
      });

      if (result.success) {
        toast({
          title: 'Registration successful!',
          description: 'Your account is pending approval. You will be notified once approved.',
        });
        navigate('/auth/pending-approval');
      } else {
        toast({
          title: 'Registration failed',
          description: result.message,
          variant: 'destructive',
        });
      }
    } catch {
      toast({
        title: 'Error',
        description: 'An unexpected error occurred. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };
  const renderStepIndicator = () => (
  <div className="flex items-center justify-center gap-2 mb-8">
    {[1, 2, 3, 4].map((s) => (
      <React.Fragment key={s}>
        <div
          className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
            s === step
              ? 'bg-primary text-primary-foreground'
              : s < step
              ? 'bg-success text-success-foreground'
              : 'bg-muted text-muted-foreground'
          }`}
        >
          {s}
        </div>
        {s < 4 && (
          <div
            className={`w-12 h-1 rounded ${
              s < step ? 'bg-success' : 'bg-muted'
            }`}
          />
        )}
      </React.Fragment>
    ))}
  </div>
);


  /* =======================
     UI (UNCHANGED)
  ======================= */

  return (
    <AuthLayout
      title="Create an account"
      subtitle={
        step === 1 ? "Let's start with your personal details" :
          step === 2 ? "Tell us about your college" :
            "Create a secure password"
      }
    >
      {renderStepIndicator()}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        {step === 1 && (
          <div className="space-y-4 animate-fade-in">
            <div className="space-y-2">
              <Label htmlFor="firstName">First Name</Label>
              <Input
                id="firstName"
                placeholder="Enter your First Name"
                {...register('firstName')}
                className={errors.firstName ? 'border-destructive' : ''}
              />
              {errors.firstName && (
                <p className="text-xs text-destructive">{errors.firstName.message}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="lastName">Last name</Label>
              <Input
                id="lastName"
                placeholder="Enter your Last Name"
                {...register('lastName')}
                className={errors.lastName ? 'border-destructive' : ''}
              />
              {errors.lastName && (
                <p className="text-xs text-destructive">{errors.lastName.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                placeholder="Enter the Email Address"
                {...register('email')}
                className={errors.email ? 'border-destructive' : ''}
              />
              {errors.email && (
                <p className="text-xs text-destructive">{errors.email.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="contactNumber">Contact Number</Label>
            
              <Input
                id="contactNumber"
                type="tel"
                placeholder="Enter your Mobile Number"
                maxLength={10}
                minLength={10}
                {...register('contactNumber')}
                className={errors.contactNumber ? 'border-destructive' : ''}
              />
              {errors.contactNumber && (
                <p className="text-xs text-destructive">{errors.contactNumber.message}</p>
              )}
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4 animate-fade-in">

            <div className="space-y-2">
              <Label htmlFor="collegeName">College Name</Label>
              <Input
                id="collegeName"
                placeholder="Enter your College Name"
                {...register('collegeName')}
                className={errors.collegeName ? 'border-destructive' : ''}
              />
              {errors.collegeName && (
                <p className="text-xs text-destructive">{errors.collegeName.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="address">Address</Label>
              <Input
                id="address"
                type="text"
                placeholder="Enter your Address"
                {...register('address')}
                className={errors.address ? 'border-destructive' : ''}
              />
              {errors.address && (
                <p className="text-xs text-destructive">{errors.address.message}</p>
              )}
            </div>

            <div className="space-y-2 flex flex-col sm:flex-row w-full">
              <div className='sm:w-1/2 w-full sm:mr-3 pt-2'>
                <Label htmlFor="city">City</Label>
                <Input
                  id="city"
                  type='text'
                  minLength={2}
                  placeholder="Enter your City"
                  {...register('city')}
                  className={errors.city ? 'border-destructive' : ''}
                />
                {errors.city && (
                  <p className="text-xs text-destructive">{errors.city.message}</p>
                )}
              </div>

              <div className='sm:w-1/2 w-full'>
                <Label htmlFor="pincode">Pincode</Label>
                <Input
                  id="pincode"
                  type='tel'
                  maxLength={6}
                  minLength={6}
                  placeholder="Enter the pincode"
                  {...register('pincode')}
                  className={errors.pincode ? 'border-destructive' : ''}
                />
                {errors.pincode && (
                  <p className="text-xs text-destructive">{errors.pincode.message}</p>
                )}
              </div>
            </div>
          </div>
        )}
        { step === 3 && (
          <div className="space-y-4 animate-fade-in">
            <div className="space-y-2">
              <Label htmlFor="courseName">Course Name</Label>
              <Input
                id="courseName"
                type="text"
                placeholder="Enter your Course Name"
                {...register('courseName')}
                className={errors.courseName ? 'border-destructive' : ''}
              />
              {errors.courseName && (
                <p className="text-xs text-destructive">{errors.courseName.message}</p>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="courseMode">Course mode</Label>
                <select
                  id="courseMode"
                  {...register('courseMode')}
                  className={`w-full border rounded px-3 py-2 ${errors.courseMode ? 'border-destructive' : ''}`}
                >
                  <option value="">Select mode</option>
                  <option value="online">Online</option>
                  <option value="offline">Offline</option>
                </select>
                {errors.courseMode && (
                  <p className="text-xs text-destructive">{String(errors.courseMode.message)}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="courseDuration">Course duration</Label>
                <select
                  id="courseDuration"
                  {...register('courseDuration')}
                  className={`w-full border rounded px-3 py-2 ${errors.courseDuration ? 'border-destructive' : ''}`}
                >
                  <option value="">Select duration</option>
                  <option value="long">Long Term</option>
                  <option value="short">Short Term</option>
                </select>
                {errors.courseDuration && (
                  <p className="text-xs text-destructive">{String(errors.courseDuration.message)}</p>
                )}
              </div>
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-4 animate-fade-in">
            {!otpSent && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-900">
                  We'll send a verification code to <strong>{email || getValues('email')}</strong>
                </p>
                <Button
                  type="button"
                  onClick={handleSendOtp}
                  disabled={isLoading}
                  className="mt-3 w-full"
                  variant="outline"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    'Send Verification Code'
                  )}
                </Button>
              </div>
            )}

            {otpSent && (
              <div className="space-y-2">
                <label htmlFor="emailOtp">Email Verification Code</label>
                <Input
                  id="emailOtp"
                  type="text"
                  placeholder="Enter the 6-digit code sent to your email"
                  {...register('emailOtp')}
                  className={errors.emailOtp ? 'border-destructive' : ''}
                  maxLength={6}
                />
                {errors.emailOtp && (
                  <p className="text-xs text-destructive">{errors.emailOtp.message}</p>
                )}
                <Button
                  type="button"
                  onClick={handleSendOtp}
                  disabled={isLoading}
                  variant="link"
                  className="p-0 h-auto text-xs"
                >
                  Resend code
                </Button>
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Create a strong password"
                  {...register('password')}
                  className={errors.password ? 'border-destructive pr-10' : 'pr-10'}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.password && (
                <p className="text-xs text-destructive">{errors.password.message}</p>
              )}
              <p className="text-xs text-muted-foreground">
                At least 8 characters with uppercase, lowercase, and number
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmPassword">Confirm Password</Label>
              <div className="relative">
                <Input
                  id="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  placeholder="Re-enter your password"
                  {...register('confirmPassword')}
                  className={errors.confirmPassword ? 'border-destructive pr-10' : 'pr-10'}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                >
                  {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.confirmPassword && (
                <p className="text-xs text-destructive">{errors.confirmPassword.message}</p>
              )}
            </div>
          </div>
        )}
        

        <div className="flex flex-col sm:flex-row gap-3 pt-2">
          {step > 1 && (
            <Button type="button" variant="outline" onClick={handleBack} className="w-full sm:flex-1">
              <ChevronLeft className="w-4 h-4" />
              Back
            </Button>
          )}
          {step < 4 ? (
            <Button type="button" onClick={handleNext} className="w-full sm:flex-1">
              Next
              <ChevronRight className="w-4 h-4" />
            </Button>
          ) : (
            <Button type="submit" className="w-full sm:flex-1" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Creating account...
                </>
              ) : (
                'Create account'
              )}
            </Button>
          )}
        </div>

        <p className="text-center text-sm text-muted-foreground">
          Already have an account?{' '}
          <Link to="/auth/login" className="text-primary font-medium hover:text-primary/80">
            Sign in
          </Link>
        </p>
      </form>
    </AuthLayout>
  );
};

export default SignupPage;
