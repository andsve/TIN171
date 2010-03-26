package soc.util;

import java.io.InputStream;
import java.util.Properties;


/**
 * Package level version file used to keep packaging and codebase in sync. The
 * file Version.java.in is filtered to create Version.java when Callisto is
 * built using <a href="http://ant.apache.org">ant</a>.  If you are not using
 * ant to build Callisto you can do this manually by copying Version.java.in
 * to Version.java, replacing "@ VERSION @" with the "version" property value
 * in the file build.xml.
 *
 * @author <a href="mailto:mchenryc@acm.org">Chadwick A. McHenry</a>
 */
public class Version {

  public static String VERSION   = "project.version";
  public static String COPYRIGHT = "project.copyright";
  
  public static String JRE_MIN_VERSION = "project.jre.min.version";
  public static String JRE_MIN_MAJOR   = "project.jre.min.major";
  public static String JRE_MIN_MINOR   = "project.jre.min.minor";
  public static String JRE_MIN_EDIT    = "project.jre.min.edit";
  
  /** Current version info */
  private static Properties versionInfo = null;

  /** ints for comparisons, concatentated and stored as JRE_MIN_VERSION */
  private static int jreMinMajor = 1;
  private static int jreMinMinor = 4;
  private static int jreMinEdit = 0;

  static {
    versionInfo = new Properties();

    // defaults in case build failed to produce version.info
    versionInfo.put(VERSION, "-error-");
    versionInfo.put(COPYRIGHT, "-error-");
    // JRE_MIN_VERSION default is built later
    try {
      String resource = "/resources/version.info";
      InputStream in = Version.class.getResourceAsStream (resource);
      versionInfo.load (in);
      in.close ();

    } catch (Exception io) {
      System.err.println ("Unable to load version information.");
      io.printStackTrace ();
    }

    // initialize concatenated value
    minJREVersion();
  }

  /** Return the current version string. */
  public static String version() {
    return versionInfo.getProperty(VERSION);
  }

  /** Return the copyright string. */
  public static String copyright() {
    return versionInfo.getProperty(COPYRIGHT);
  }

  /** Return the minimum required jre. */
  public static String minJREVersion() {
    String jreMinVersion = versionInfo.getProperty(JRE_MIN_VERSION);
    if (jreMinVersion == null) {
      try {
        String major = versionInfo.getProperty(JRE_MIN_MAJOR, ""+jreMinMajor);
        String minor = versionInfo.getProperty(JRE_MIN_MINOR, ""+jreMinMinor);
        String edit  = versionInfo.getProperty(JRE_MIN_EDIT,  ""+jreMinEdit);
        jreMinMajor = Integer.parseInt(major);
        jreMinMinor = Integer.parseInt(minor);
        jreMinEdit  = Integer.parseInt(edit);
        
      } catch(Exception x) { // NPE or NumberFormat uses default values
        System.err.println("Error retrieving Version info: ");
        x.printStackTrace();
      }

      jreMinVersion = jreMinMajor+"."+jreMinMinor+"."+jreMinEdit;
      versionInfo.put(JRE_MIN_VERSION, jreMinVersion);
    }
    return jreMinVersion;
  }

  /** Check for sufficient version of the JRE. */
  static boolean isJREValid () {
    String v = System.getProperty("java.vm.version");
    int major = Integer.parseInt (v.substring (0,1));
    int minor = Integer.parseInt (v.substring (2,3));
    int edit = Integer.parseInt (v.substring (4,5));;
    String build = v.substring (6);

    if (versionInfo.getProperty(JRE_MIN_VERSION) == null)
      minJREVersion();  
    
    return (major >= jreMinMajor || minor >= jreMinMinor || edit >= jreMinEdit);
  }
}
