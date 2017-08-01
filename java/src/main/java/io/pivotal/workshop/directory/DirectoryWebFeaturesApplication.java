package io.pivotal.workshop.directory;

import java.util.stream.Stream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.Banner;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class DirectoryWebFeaturesApplication {

  public static void main(String[] args) {

    SpringApplication app = new SpringApplication(DirectoryWebFeaturesApplication.class);
    app.setBannerMode(Banner.Mode.OFF);
//    app.setWebEnvironment(false);
    app.run(args);
  }

  private static final Logger log = LoggerFactory.getLogger("[ARGUMENTS]");

  @Bean
  public CommandLineRunner commandRunner() {
    return args -> Stream.of(args).forEach(s -> log.info("CommandLine: " + s));
  }
}
