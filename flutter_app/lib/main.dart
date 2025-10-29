import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:supabase_auth_ui/supabase_auth_ui.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Supabase.initialize(
    url: 'https://nxzaxhgyzapnnqcfjxpn.supabase.co',
    anonKey: 'YOUR_ANON_KEY_HERE',
  );
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Supabase Auth Demo',
      home: Scaffold(
        body: Center(
          child: SupaEmailAuth(
            redirectTo: kIsWeb ? null : 'io.yourapp://callback',
            onSignInComplete: (response) {
              // navigate to your /recipes page or any home page
              Navigator.of(context).pushReplacementNamed('/recipes');
            },
            onSignUpComplete: (response) {
              // handle signup
            },
          ),
        ),
      ),
    );
  }
}
