package io.pivotal.workshop.directory;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;

@SpringBootApplication
public class DirectoryWebFeaturesApplication {
  public static void main(String[] args) {
    SpringApplicationBuilder app = new SpringApplicationBuilder(DirectoryWebFeaturesApplication.class);
    app.build().run(args);
  }
}
