#include <gio/gio.h>
#include <stdio.h>

GVariant *build_var()
{
    GVariantBuilder *builder;
    GVariant *value;

    builder = g_variant_builder_new (G_VARIANT_TYPE ("(osa{sv})"));
    g_variant_builder_add (builder, "o", "/bluez/yaptb/btkb_profile");
    g_variant_builder_add (builder, "s", "00001124-0000-1000-8000-00805f9b34fb");
    g_variant_builder_open (builder, G_VARIANT_TYPE ("a{sv}"));
    g_variant_builder_add (builder, "{sv}", "ServiceRecord", g_variant_new_string ("<xml></xml>"));
    g_variant_builder_add (builder, "{sv}", "Role", g_variant_new_string ("server"));
    g_variant_builder_add (builder, "{sv}", "RequireAuthentication", g_variant_new_boolean(0));
    g_variant_builder_add (builder, "{sv}", "RequireAuthorization", g_variant_new_boolean(0));
    g_variant_builder_close (builder);
    value = g_variant_builder_end (builder);
    g_variant_builder_unref (builder);
    return value;
}

int main() 
{
    GDBusConnection *connection;
    GError *err = NULL;
    connection = g_bus_get_sync(G_BUS_TYPE_SYSTEM, NULL, &err);
    if (err != NULL) {
        fprintf (stderr, "Unable to read file: %s\n", err->message);
        return -1;
    }
    int value = 0;
    g_dbus_connection_call_sync (connection,
                                "org.bluez",
                                "/org/bluez",
                                "org.bluez.ProfileManager1",
                                "RegisterProfile",
                                // g_variant_new("(os)",
                                //     "/bluez/yaptb/btkb_profile",
                                //     "00001124-0000-1000-8000-00805f9b34fb"
                                // ),
                                build_var(),
                                NULL,
                                G_DBUS_CALL_FLAGS_NONE,
                                -1,
                                NULL,
                                &err);
    return 0;
}