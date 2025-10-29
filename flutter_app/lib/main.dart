import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:supabase_auth_ui/supabase_auth_ui.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Supabase.initialize(
    url: 'https://nxzaxhgyzapnnqcfjxpn.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im54emF4aGd5emFwbm5xY2ZqeHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAxMTQzMTIsImV4cCI6MjA3NTY5MDMxMn0.bzW-RrlsyoZvvfWLh3YpZ0DO7WTKlNwEMSDK1V_3joc',
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
