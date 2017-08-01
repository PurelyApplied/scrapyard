package io.pivotal.workshop.directory.config;

import io.pivotal.workshop.directory.aop.SimpleAudit;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class DirectoryConfig {

  @ConditionalOnClass(name={"io.pivotal.workshop.directory.DirectoryRepository"})
  @Bean
  public SimpleAudit simpleAudit(){
    return new SimpleAudit();
  }

}
